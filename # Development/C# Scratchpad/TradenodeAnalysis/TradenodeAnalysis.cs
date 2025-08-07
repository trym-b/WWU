using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace EU4_Scratchpad.TradenodeAnalysis;

public static class TradeNodeAnalyzer
{
    private static Dictionary<string, List<string>> graph = new();
    private static Dictionary<string, List<string>> reverseGraph = new(); // not strictly needed
    private static Dictionary<string, List<string>> rawNodeContents = new(); // full node content
    private static HashSet<string> definedNodes = new();
    private static List<(string from, string to)> unresolvedEdges = new();

    public static void Load(string filePath)
    {
        string[] lines = File.ReadAllLines(filePath);
        ParseTradeNodes(lines);
    }

    private static void ParseTradeNodes(string[] lines)
    {
        string currentNode = null;
        List<string> currentNodeLines = null;
        Stack<int> braceLineStack = new(); // stores line numbers of unmatched '{'

        for (int i = 0; i < lines.Length; i++)
        {
            string line = lines[i];
            string trimmed = line.Trim();

            if (string.IsNullOrWhiteSpace(trimmed) || trimmed.StartsWith("#"))
                continue;

            // Start of a node
            if (trimmed.StartsWith("node_") && trimmed.Contains("="))
            {
                int idx = trimmed.IndexOf('=');
                currentNode = trimmed.Substring(0, idx).Trim();

                if (definedNodes.Contains(currentNode))
                {
                    Console.WriteLine($"⚠️  Warning: Duplicate node '{currentNode}' at line {i + 1}");
                }

                definedNodes.Add(currentNode);
                graph[currentNode] = new List<string>();
                reverseGraph[currentNode] = new List<string>();
                currentNodeLines = new List<string>();
                rawNodeContents[currentNode] = currentNodeLines;
            }

            if (currentNode != null)
                currentNodeLines?.Add(line);

            // Brace tracking
            for (int j = 0; j < line.Length; j++)
            {
                if (line[j] == '{')
                    braceLineStack.Push(i + 1); // line number
                else if (line[j] == '}')
                {
                    if (braceLineStack.Count > 0)
                        braceLineStack.Pop();
                    else
                        Console.WriteLine($"❌ Syntax Error: Unmatched closing brace '}}' at line {i + 1}");
                }
            }

            // Multiline outgoing block
            if (currentNode != null && trimmed.StartsWith("outgoing"))
            {
                int outgoingBraceDepth = CountChar(line, '{') - CountChar(line, '}');
                List<string> outgoingBlock = new List<string> { line };

                int startLine = i;

                while (outgoingBraceDepth > 0 && i + 1 < lines.Length)
                {
                    i++;
                    string nextLine = lines[i];
                    outgoingBlock.Add(nextLine);
                    outgoingBraceDepth += CountChar(nextLine, '{');
                    outgoingBraceDepth -= CountChar(nextLine, '}');

                    for (int j = 0; j < nextLine.Length; j++)
                    {
                        if (nextLine[j] == '{')
                            braceLineStack.Push(i + 1);
                        else if (nextLine[j] == '}')
                        {
                            if (braceLineStack.Count > 0)
                                braceLineStack.Pop();
                            else
                                Console.WriteLine($"❌ Syntax Error: Unmatched closing brace '}}' at line {i + 1}");
                        }
                    }
                }

                // ✅ Append full outgoing block to the node's lines
                if (currentNodeLines != null)
                {
                    currentNodeLines.AddRange(outgoingBlock.Skip(1)); // Skip the first line since it's already added
                }

                string outgoingText = string.Join("\n", outgoingBlock);
                var match = Regex.Match(outgoingText, @"name\s*=\s*""([^""]+)""");
                if (match.Success)
                {
                    string target = match.Groups[1].Value;
                    graph[currentNode].Add(target);

                    if (!reverseGraph.ContainsKey(target))
                        reverseGraph[target] = new List<string>();
                    reverseGraph[target].Add(currentNode);

                    unresolvedEdges.Add((currentNode, target));
                }
                else
                {
                    Console.WriteLine($"❌ Syntax Error: Could not find name in outgoing block starting at line {i + 1 - outgoingBlock.Count}");
                }
            }
        }

        if (braceLineStack.Count > 0)
        {
            Console.WriteLine($"❌ Syntax Error: {braceLineStack.Count} unmatched opening brace(s):");
            foreach (int lineNum in braceLineStack)
            {
                Console.WriteLine($"   ↪ Missing closing brace for '{{' opened at line {lineNum}");
            }
        }

        foreach (var (from, to) in unresolvedEdges)
        {
            if (!graph.ContainsKey(to))
                Console.WriteLine($"⚠️  Warning: Node '{from}' has outgoing to undefined node '{to}'");
        }
    }

    private static int CountChar(string line, char c)
    {
        int count = 0;
        foreach (char ch in line)
            if (ch == c) count++;
        return count;
    }

    public static void DetectCycles()
    {
        var visited = new HashSet<string>();
        var recStack = new HashSet<string>();

        foreach (var node in graph.Keys)
        {
            if (DetectCycleUtil(node, visited, recStack, new Stack<string>()))
                return;
        }

        Console.WriteLine("✅ No trade loops detected.");
    }

    private static bool DetectCycleUtil(string node, HashSet<string> visited, HashSet<string> recStack, Stack<string> path)
    {
        if (recStack.Contains(node))
        {
            Console.WriteLine("❌ Trade loop detected:");
            foreach (var n in path)
                Console.Write(n + " -> ");
            Console.WriteLine(node);
            return true;
        }

        if (visited.Contains(node))
            return false;

        visited.Add(node);
        recStack.Add(node);
        path.Push(node);

        foreach (var neighbor in graph[node])
        {
            if (DetectCycleUtil(neighbor, visited, recStack, path))
                return true;
        }

        recStack.Remove(node);
        path.Pop();
        return false;
    }

    public static void WriteSortedTradeNodes(string outputPath)
    {
        var sorted = TopologicalSort();
        if (sorted == null)
        {
            Console.WriteLine("❌ Cannot write output due to trade loop.");
            return;
        }

        using StreamWriter writer = new(outputPath, false, Encoding.UTF8);
        foreach (string node in sorted)
        {
            if (rawNodeContents.TryGetValue(node, out var lines))
            {
                foreach (var line in lines)
                    writer.WriteLine(line);
                writer.WriteLine(); // separate entries with a newline
            }
            else
            {
                Console.WriteLine($"⚠️  Missing content for node '{node}', skipping.");
            }
        }

        Console.WriteLine($"✅ Sorted trade nodes written to '{outputPath}'.");
    }

    private static List<string> TopologicalSort()
    {
        var visited = new HashSet<string>();
        var tempMarked = new HashSet<string>();
        var result = new List<string>();

        bool Visit(string node)
        {
            if (tempMarked.Contains(node))
            {
                Console.WriteLine($"❌ Cycle detected while sorting at node: {node}");
                return false;
            }

            if (!visited.Contains(node))
            {
                tempMarked.Add(node);
                if (graph.TryGetValue(node, out var neighbors))
                {
                    foreach (var neighbor in neighbors)
                    {
                        if (!Visit(neighbor))
                            return false;
                    }
                }
                tempMarked.Remove(node);
                visited.Add(node);
                result.Add(node);
            }

            return true;
        }

        foreach (var node in graph.Keys)
        {
            if (!visited.Contains(node))
            {
                if (!Visit(node))
                    return null;
            }
        }

        result.Reverse(); // We built it in reverse order
        return result;
    }

    public static void Apply()
    {
        var folder = @"C:\Users\benja\Documents\Paradox Interactive\Europa Universalis IV\mod\WWU-Old\common\tradenodes\";
        var path = Path.Combine(folder, "00_tradenodes.txt");
        var write = Path.Combine(folder, "00_tradenodes_sorted.txt");

        try
        {
            Load(path);
            DetectCycles();
            //WriteSortedTradeNodes(write);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Fatal Error: {ex.Message}");
        }
    }
}