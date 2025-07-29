using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace EU4_Scratchpad.Unit_Generator;

public class UnitGeneratorData
{
    public List<UnitBase> UnitBase { get; set; }
    public List<OutputGroup> OutputGroup { get; set; }
}

public class OutputGroup
{
    public string name { get; set; }
    public string displayName { get; set; }
    public List<int> inf_a_modifier { get; set; }
    public List<int> inf_b_modifier { get; set; }
    public List<int> inf_c_modifier { get; set; }
    public List<int> cav_a_modifier { get; set; }
    public List<int> cav_b_modifier { get; set; }
    public List<int> art_a_modifier { get; set; }
    public List<int> art_b_modifier { get; set; }
}

public class UnitBase
{
    public string name { get; set; }
    public string type { get; set; }
    public List<int> stats { get; set; }
    public string displayName { get; set; }
    public int manpower { get; set; }
    public int tier { get; set; }
    public string iconString { get; set; }
}

