from pathlib import Path

from lark import Lark, Transformer


class EventAndMissionModifierParser(Transformer):
    def NUMBER(self, args) -> float | int:
        my_float = float(args.value)
        if my_float.is_integer():
            return int(my_float)
        return my_float

    def SIGNED_NUMBER(self, args) -> float:
        return float(args.value)

    def value(self, args):
        return args[0]

    def object(self, args) -> dict:
        res = {}
        for i in args:
            res.update(i)
        return res

    def WORDS_WITH_UNDERSCORE(self, args) -> str:
        return str(args.value)

    def single_assignment(self, args) -> dict:
        return {args[0]: args[1]}

    def repeated_assignments(self, args) -> dict:
        res = {}
        for i in args:
            res.update(i)
        return res

    def starts_with_number(self, args) -> str:
        return f"{args[0]}_{args[1]}"

    def ESCAPED_STRING(self, args) -> str:
        return args[1]


def parse_text(text: str) -> Lark:
    lark_file = Path(__file__).parent.resolve() / "event_and_mission_modifier.lark"
    event_and_mission_modifier_parser = Lark(
        lark_file.read_text(encoding="utf-8"), start="repeated_assignments"
    )
    return event_and_mission_modifier_parser.parse(
        text,
    )


def transform(tree: Lark) -> dict:
    return EventAndMissionModifierParser().transform(tree)
