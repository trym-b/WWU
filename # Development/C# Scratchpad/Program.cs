using EU4_Scratchpad.Unit_Generator;
using System.ComponentModel.DataAnnotations;

namespace EU4_Scratchpad
{
    internal class Program
    {
        static void Main(string[] args)
        {
            SetupOutputFolder();

            UnitGenerator.GenerateUnits();
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
