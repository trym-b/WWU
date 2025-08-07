using EU4_Scratchpad.Draenor_Collapse;
using EU4_Scratchpad.TradenodeAnalysis;

namespace EU4_Scratchpad
{
    internal class Program
    {
        static void Main(string[] args)
        {
            SetupOutputFolder();

            TradeNodeAnalyzer.Apply();
        }

        public static void SetupOutputFolder()
        {
            var outputDir = Path.Combine(AppContext.BaseDirectory, "Output");

            if (!Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }
        }

    }
}
