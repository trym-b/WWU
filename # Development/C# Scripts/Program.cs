using System.ComponentModel.DataAnnotations;

namespace EU4_Scratchpad
{
    internal class Program
    {
        static void Main(string[] args)
        {
            SetupOutputFolder();


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
