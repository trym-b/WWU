using EU4_Scratchpad.Unit_Generator;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace EU4_Scratchpad;

[JsonSourceGenerationOptions(
    WriteIndented = true,
    GenerationMode = JsonSourceGenerationMode.Metadata,
    IncludeFields = true)]

[JsonSerializable(typeof(UnitGeneratorData))]
internal partial class DataSerializerContext : JsonSerializerContext
{
}

