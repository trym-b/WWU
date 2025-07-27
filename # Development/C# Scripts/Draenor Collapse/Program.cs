using System.ComponentModel.DataAnnotations;

namespace EU4_Scratchpad
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var outputDir = Path.Combine(AppContext.BaseDirectory, "Output");

            if(!Directory.Exists(outputDir) )
            {
                Directory.CreateDirectory(outputDir);
            }

            SpawnInfantryCode();
            //BaseTaxCode();
            //DraenorProvinceTransfer();
        }

        public static void SpawnInfantryCode()
        {
            var outputStr = "spawn_infantry_based_on_province_count = {\r\n";

            for (int i = 1; i < 100; i++)
            {
                var min = i;

                var template = "" +
                "\tif = {\r\n" +
                "\t\tlimit = {\r\n" +
                "\t\t\tROOT = {\r\n" +
                $"\t\t\t\tnum_of_cities = {min}\r\n" +
                "\t\t\t}\r\n" +
                "\t\t}\r\n" +
                "\t\t\r\n" +
                $"\t\tcapital_scope = {{ infantry = ROOT }}\r\n" +
                "\t}\r\n";

                outputStr = outputStr + template;
            }

            var writePath = Path.Combine(AppContext.BaseDirectory, "Output", $"spawn_infantry_based_on_province_count.txt");
            File.WriteAllText(writePath, outputStr);
        }

        public static void BaseTaxCode()
        {
            var type = "base_tax";
            var outputStr = "copy_over_base_tax = {\r\n";

            for (int i = 1; i < 1000; i++)
            {
                var min = i;
                var max = i + 1;

                var template = "" +
                "\telse_if = {\r\n" +
                "\t\tlimit = {\r\n" +
                "\t\t\tevent_target:cur_province = {\r\n" +
                $"\t\t\t\t{type} = {min}\r\n" +
                $"\t\t\t\tNOT = {{ {type} = {max} }}\r\n" +
                "\t\t\t}\r\n" +
                "\t\t}\r\n" +
                "\t\t\r\n" +
                $"\t\tset_{type} = {min}\r\n" +
                "\t}\r\n";

                if (i == 1)
                {
                    template = template.Replace("else_if", "if");
                }


                outputStr = outputStr + template;
            }

            var writePath = Path.Combine(AppContext.BaseDirectory, "Output", $"{type}.txt");
            File.WriteAllText(writePath, outputStr);
        }

        public static void DraenorProvinceTransfer()
        {
            var mappingPath = Path.Combine(AppContext.BaseDirectory, "Assets", "province_mapping.txt");
            var fileContents = File.ReadAllText(mappingPath);

            var outputPath = Path.Combine(AppContext.BaseDirectory, "Output", "draenor_collapse.txt");

            var mappingDict = new Dictionary<string, List<string>>();

            // Get mappings
            var lines = fileContents.Split("\n");
            foreach (var line in lines)
            {
                var mapping = line.Split(";");
                var baseId = mapping[0].Trim();
                var newIds = mapping[1].Trim();

                var newIdList = new List<string>();

                if (newIds.Contains(","))
                {
                    newIdList = newIds.Split(",").ToList();
                }
                else
                {
                    newIdList = new List<string>()
                    {
                        newIds
                    };
                }

                if (!mappingDict.ContainsKey(baseId))
                {
                    mappingDict.Add(baseId, newIdList);
                }
                else
                {
                    Console.WriteLine($"Duplicate base key: {baseId}");
                }
            }

            // Output code
            var outputStr = "apply_province_transfer_to_outland = {\r\n";

            foreach (var entry in mappingDict)
            {
                var sourceId = entry.Key;
                var targetIds = entry.Value;

                var sourceTemplate = "" +
                    $"\t# Source: {sourceId}\r\n" +
                    $"\t{sourceId} = {{\r\n" +
                    "\t\tsave_event_target_as = cur_province\r\n" +
                    "\t\t\r\n" +
                    "\t\towner = {\r\n" +
                    "\t\t\tsave_event_target_as = cur_province_owner\r\n" +
                    "\t\t}\r\n" +
                    "\t}\r\n";

                outputStr = outputStr + sourceTemplate;

                foreach (var id in targetIds)
                {
                    var targetTemplate = "" +
                        $"\t# Target: {id}\r\n" +
                        $"\t{id} = {{\r\n" +
                        "\t\tcede_province = event_target:cur_province_owner\r\n" +
                        "\t\tadd_core = event_target:cur_province_owner\r\n" +
                        "\t\tchange_culture = event_target:cur_province_owner\r\n" +
                        "\t\tchange_religion = event_target:cur_province_owner\r\n" +
                        "\t\t\r\n" +
                        "\t\tcopy_over_base_tax = yes\r\n" +
                        "\t\tcopy_over_base_production = yes\r\n" +
                        "\t\tcopy_over_base_manpower = yes\r\n" +
                        "\t}\r\n";

                    outputStr = outputStr + targetTemplate;
                }

                outputStr = outputStr + "\r\n\r\n";
            }

            outputStr = outputStr + "}\r\n";

            File.WriteAllText(outputPath, outputStr);
        }
    }
}
