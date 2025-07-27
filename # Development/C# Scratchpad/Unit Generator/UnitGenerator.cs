using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace EU4_Scratchpad.Unit_Generator;

public static class UnitGenerator
{
    public static void GenerateUnits()
    {
        var unitData = GetUnitData();

        if (unitData == null)
            return;

        GenerateUnitFiles(unitData);
        GenerateUnitLocalisation(unitData);
        GenerateUnitTechnologyEntries(unitData);
    }

    public static void GenerateUnitFiles(UnitGeneratorData data)
    {
        var writeDir = Path.Combine(AppContext.BaseDirectory, "Output", "units");

        if(!Directory.Exists(writeDir))
        {
            Directory.CreateDirectory(writeDir);
        }

        foreach (var group in data.OutputGroup)
        {
            var prettyName = group.name.Replace("tech_", "");

            foreach (var unit in data.UnitBase)
            {
                var outputStr = "";

                List<int> modifiers = null;

                var offensiveMorale = unit.stats[0];
                var defensiveMorale = unit.stats[1];
                var offensiveFire = unit.stats[2];
                var defensiveFire = unit.stats[3];
                var offensiveShock = unit.stats[4];
                var defensiveShock = unit.stats[5];
                var manuever = unit.stats[6];

                if(unit.name.Contains("inf_a"))
                {
                    modifiers = group.inf_a_modifier;
                }
                if (unit.name.Contains("inf_b"))
                {
                    modifiers = group.inf_b_modifier;
                }
                if (unit.name.Contains("inf_c"))
                {
                    modifiers = group.inf_c_modifier;
                }
                if (unit.name.Contains("cav_a"))
                {
                    modifiers = group.cav_a_modifier;
                }
                if (unit.name.Contains("cav_b"))
                {
                    modifiers = group.cav_b_modifier;
                }
                if (unit.name.Contains("art_a"))
                {
                    modifiers = group.art_a_modifier;
                }
                if (unit.name.Contains("art_b"))
                {
                    modifiers = group.art_b_modifier;
                }

                if (modifiers != null)
                {
                    offensiveMorale += modifiers[0];
                    defensiveMorale += modifiers[1];
                    offensiveFire += modifiers[2];
                    defensiveFire += modifiers[3];
                    offensiveShock += modifiers[4];
                    defensiveShock += modifiers[5];
                    manuever += modifiers[6];
                }

                if (offensiveMorale < 0)
                    offensiveMorale = 0;

                if (defensiveMorale < 0)
                    defensiveMorale = 0;

                if (offensiveFire < 0)
                    offensiveFire = 0;

                if (defensiveFire < 0)
                    defensiveFire = 0;

                if (offensiveShock < 0)
                    offensiveShock = 0;

                if (defensiveShock < 0)
                    defensiveShock = 0;

                if (manuever < 0)
                    manuever = 0;

                outputStr = "" +
                    $"type = {unit.type}\n" +
                    $"unit_type = {group.name}\n" +
                    "\n" +
                    $"maneuver = {manuever}\n" +
                    $"offensive_morale = {offensiveMorale}\n" +
                    $"defensive_morale = {defensiveMorale}\n" +
                    $"offensive_fire = {offensiveFire}\n" +
                    $"defensive_fire = {defensiveFire}\n" +
                    $"offensive_shock = {offensiveShock}\n" +
                    $"defensive_shock = {defensiveShock}\n";

                var writePath = Path.Combine(AppContext.BaseDirectory, "Output", "units", $"{prettyName}_{unit.name}.txt");

                File.WriteAllText(writePath, outputStr);
            }
        }
    }

    public static void GenerateUnitLocalisation(UnitGeneratorData data)
    {
        var writePath = Path.Combine(AppContext.BaseDirectory, "Output", "unit_generator___localisation.yml");

        var outputStr = "";

        foreach (var group in data.OutputGroup)
        {
            foreach (var unit in data.UnitBase)
            {
                outputStr = outputStr + $" {group.name}_{unit.name}: \"£{unit.iconString}£ {group.displayName} {unit.displayName}\"\n";
                outputStr = outputStr + $" {group.name}_{unit.name}DESCR: \"\"\n";
            }

            outputStr = outputStr + $"\n";
        }

        File.WriteAllText(writePath, outputStr);
    }

    public static void GenerateUnitTechnologyEntries(UnitGeneratorData data)
    {
        var writePath = Path.Combine(AppContext.BaseDirectory, "Output", "unit_generator__mil_entries.txt");

        Dictionary<int, string> blocks = new Dictionary<int, string>()
        {
            { 1, "" },
            { 2, "" },
            { 3, "" },
            { 4, "" },
            { 5, "" },
        };

        foreach (var group in data.OutputGroup)
        {
            var prettyName = group.name.Replace("tech_", "");

            foreach (var unit in data.UnitBase)
            {
                var str = blocks[unit.tier];

                str = str + $"enable = {prettyName}_{unit.name}\n";

                blocks[unit.tier] = str;
            }
        }

        var outputStr = "";

        foreach(var block in blocks)
        {
            outputStr += block.Value + "\n";
        }

        File.WriteAllText(writePath, outputStr);
    }

    public static UnitGeneratorData GetUnitData()
    {
        UnitGeneratorData data = null;

        var dataPath = Path.Combine(AppContext.BaseDirectory, "Assets", "unit_generator_data.json");

        if (File.Exists(dataPath))
        {
            try
            {
                var filestring = File.ReadAllText(dataPath);
                var options = new JsonSerializerOptions();

                data = JsonSerializer.Deserialize(filestring, DataSerializerContext.Default.UnitGeneratorData);

                if (data == null)
                {
                    throw new Exception("JsonConvert returned null");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Failed to read unit_generator_data.json: {e}");
            }
        }

        return data;
    }
}
