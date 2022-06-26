from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dataclasses import dataclass, fields
from re import match, search


@dataclass(frozen=True)
class Language:
    name: str
    code: str
    paradox_localization_key: str


@dataclass
class LanguageCollection:
    english: Language = Language(
        name="english",
        code="en",
        paradox_localization_key="l_english",
    )
    german: Language = Language(
        name="german",
        code="de",
        paradox_localization_key="l_german",
    )
    spanish: Language = Language(
        name="spanish",
        code="es",
        paradox_localization_key="l_spanish",
    )
    french: Language = Language(
        name="french",
        code="fr",
        paradox_localization_key="l_french",
    )


def _ignored_key_patterns(language: Language) -> list[str]:
    if language == LanguageCollection.german:
        return [
            r"^artifact_icon_\S*$",
            r"^class_icon_\S*$",
            r"^portrait_\S*$",
            r"^NOT_DISCOVERED_\S*$",
            r"^LOCATION_OF_\S*$",
            r"^IS_PRIMARY_ARTIFACT_\S*$",
            r"^artifact_name_\S*$",
            r"^wwu_artifact_repository.1.option.location_view.\S*$",
            r"^wwu_artifact_repository.\d.option.ebonchill$",
            r"^culture_\S*$",
            r"^\S*_gfx$",
            r"^SKILL_MANA_\d$",
            r"^SKILL_RANK_\S*$",
        ]
    if language == LanguageCollection.spanish:
        return [
            r"^artifact_icon_\S*$",
            r"^class_icon_\S*$",
            r"^portrait_\S*$",
            r"^NOT_DISCOVERED_\S*$",
            r"^LOCATION_OF_\S*$",
            r"^IS_PRIMARY_ARTIFACT_\S*$",
            r"^artifact_name_\S*$",
            r"^wwu_artifact_repository.1.option.location_view.\S*$",
            r"^culture_\S*$",
            r"^\S*_gfx$",
            r"^SKILL_MANA_\d$",
            r"^SKILL_RANK_\S*$",
        ]
    if language == LanguageCollection.french:
        return [
            r"^artifact_icon_\S*$",
            r"^class_icon_\S*$",
            r"^portrait_\S*$",
            r"^NOT_DISCOVERED_\S*$",
            r"^LOCATION_OF_\S*$",
            r"^IS_PRIMARY_ARTIFACT_\S*$",
            r"^artifact_name_\S*$",
            r"^wwu_artifact_repository.1.option.location_view.\S*$",
            r"^culture_\S*$",
            r"^\S*_gfx$",
            r"^SKILL_MANA_\d$",
            r"^SKILL_RANK_\S*$",
        ]
    raise RuntimeError(f"Unsupported language: {language}")


def _ignored_keys(language: Language) -> list[str]:
    if language == LanguageCollection.german:
        return [
            "immortal_life_text",
            "long_life_text",
            "normal_life_text",
            "artifact_ebonchill",
            "CONTINENTAL_WAR_NAME",
            "wwu_archaeology.26.desc",
            "estate_traders_colonise_X_requirements",
            "estate_traders_colonise_more_X_requirements",
            "estate_nobility_supremacy_over_government_effect_tooltip",
            "estate_traders_indebted_to_merchants_effect_tooltip",
            "COUNCIL",
            "angrathar",
            "desc_embraced_magic",
            "desc_murloc_muster",
            "faction_lichs",
            "mechanic_enables_decadence_event",
            "mechanic_enables_heir_apparent_event",
            "mechanic_enables_gavelkind_succession_event",
            "mechanic_enables_puppet_event",
            "mechanic_enables_bonus_on_relection_event",
            "mechanic_enables_organisational_focus_event",
            "mechanic_enables_ransom_captives_event",
            "mechanic_enables_enslave_captives_event",
            "mechanic_enables_integrate_captives_event",
            "mechanic_enables_execute_captives_event",
            "mechanic_enables_conscript_captives_event",
            "mechanic_enables_spoiled_victor_event",
            "mechanic_enables_warsong_event",
            "tinker_republic_reform",
            "tinker_republic_legacy",
            "wwu_labor_tier_commission",
            "sg_military",
            "sg_military_MECHANIC_TOOLTIP",
            "orc_gfx_sprite_packL",
            "worgen_gfx_sprite_pack",
            "gp_gadgetzan",
            "gp_acherus",
            "gp_sporeggar",
            "gp_isildien",
        ]
    if language == LanguageCollection.spanish:
        return []
    if language == LanguageCollection.french:
        return []
    raise RuntimeError(f"Unsupported language: {language}")


def _ignored_values(language: Language) -> list[str]:
    if language == LanguageCollection.german:
        return [
            "Hurrah!",
        ]
    if language == LanguageCollection.spanish:
        return []
    if language == LanguageCollection.french:
        return []
    raise RuntimeError(f"Unsupported language: {language}")


def is_key_ignored(key: str, target_language: Language) -> bool:
    for ignore_pattern in _ignored_key_patterns(target_language):
        if match(ignore_pattern, key):
            return True
    if key in _ignored_keys(target_language):
        return True
    return False


def is_value_ignored(value: str, target_language: Language) -> bool:
    if value in _ignored_values(target_language):
        return True
    result = search(r"[A-Za-z]+", value)
    if result:
        return False
    return True


def source_language() -> Language:
    return LanguageCollection.english


def target_language(language_as_string: str) -> Language:
    if language_as_string == LanguageCollection.german.name:
        return LanguageCollection.german
    if language_as_string == LanguageCollection.spanish.name:
        return LanguageCollection.spanish
    if language_as_string == LanguageCollection.french.name:
        return LanguageCollection.french
    raise ArgumentTypeError(
        f"Invalid language: {language_as_string}, valid options: {' '.join([f.name for f in fields(LanguageCollection)])}"
    )
