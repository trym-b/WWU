#--------------------------------------
# Stormwind
#--------------------------------------
#STW_stormwind_column_1 = {
	slot = 1
	generic = no
	ai = yes
    has_country_shield = yes
    
	potential = {
		tag = STW
		has_country_flag = stormwind_one_finished
	}

	STW_stormwind_reclaim_stonecairn = { 
		icon = mission_runestone
        position = 2
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_calm_subjects } 
        
		trigger = {
            area_stonecairn = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
            area_eastvale = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
		}
        provinces_to_highlight = {
            OR = {
				area = area_stonecairn
				area = area_eastvale
			}
        }
		effect = { 
			every_province = {
			    limit = {
				    OR = {
					    area = area_stonecairn
						area = area_eastvale
					}
				}
				change_culture = ROOT
			}
		}
	}

	STW_stormwind_secure_westfall_shore = { 
		icon = mission_storehouse
        position = 4
		required_missions = { STW_stormwind_unite_azerothian_lands } 
        
		trigger = {
            area_westfall_shore = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
		}
        provinces_to_highlight = {
            area = area_westfall_shore
        }
		effect = { 
			add_country_modifier = {
				name = "mission_secured_westfall_shore"
				duration = -1
			}
		}
	}

	STW_stormwind_army_reform = {
		icon = mission_titan_spirits
		position = 5

		trigger = {
			army_size = 50
			army_tradition = 50
			army_professionalism = 0.25
		}

		effect = {
			country_event = { id = wwu_mission_stw_main.1 }
		}
	}

	STW_stormwind_order_of_knights = {
		icon = mission_titan_spirits
		position = 6

		required_missions = { STW_stormwind_army_reform }

		trigger = {
			army_professionalism = 0.5
			army_tradition = 75
			cavalry_fraction = 0.2
			has_global_modifier_value = {
				which = cavalry_power
				value = 0.15
			}
		}

		effect = {
			custom_tooltip = SPECIALIST_BROTHERHOOD_TT
			set_country_flag = stormwind_avalable_horsebrothers

			custom_tooltip = ENABLE_PRIVILIEGE_LORDS_ON_HORSES_TT
			set_country_flag = stormwind_enable_privilige_lords_on_horses

			add_country_modifier = {
				name = mission_cavalry_expansion
				duration = -1
			}
		}
	}

    STW_stormwind_faith_and_magic = {
        icon = mission_titan_spirits
        position = 7

        required_missions = { STW_stormwind_order_of_knights }

        trigger = {
			2204 = {
				has_great_project = {
					type = gp_cathedral_of_light
					tier = 2
				}
			}
			2205 = {
				has_great_project = {
					type = gp_stormwind_mage_tower
					tier = 2
				}
			}
            OR = {
                innovativeness = 75
                religious_unity = 0.9
            }
        }

        provinces_to_highlight = {
            OR = {
                province_id = 2205
                province_id = 2204
            }
        }

        effect = {
            country_event = { id = wwu_mission_stw_main.2 }
        }
    }
}

#STW_stormwind_column_2 = {
	slot = 2
	generic = no
	ai = yes
    has_country_shield = yes
    
	potential = {
		tag = STW
		has_country_flag = stormwind_one_finished
	}
    
    STW_stormwind_calm_subjects = { 
		icon = mission_paladin_empowered_seals_righteous
        position = 1
		required_missions = {  } 
        
		trigger = {
            if = {
                limit = {
                    overlord_of = WST
                }
                WST = {
                    NOT = { liberty_desire = 10 }
                }
            }
            if = {
                limit = {
                    overlord_of = DKS
                }
                DKS = {
                    NOT = { liberty_desire = 10 }
                }
            }
            if = {
                limit = {
                    overlord_of = RRG
                }
                RRG = {
                    NOT = { liberty_desire = 10 }
                }
            }
            if = {
                limit = {
                    overlord_of = P59
                }
                P59 = {
                    NOT = { liberty_desire = 10 }
                }
            }
		}
		effect = { 
            if = {
                limit = { overlord_of = WST }
                
                WST = {
                    add_country_modifier = {
                        name = mission_subject_support
                        duration = 9125
                    }
                }
            }
            if = {
                limit = { overlord_of = DKS }
                
                DKS = {
                    add_country_modifier = {
                        name = mission_subject_support
                        duration = 9125
                    }
                }
            }
            if = {
                limit = { overlord_of = RRG }
                
                RRG = {
                    add_country_modifier = {
                        name = mission_subject_support
                        duration = 9125
                    }
                }
            }
            if = {
                limit = { overlord_of = P59 }
                
                P59 = {
                    add_country_modifier = {
                        name = mission_subject_support
                        duration = 9125
                    }
                }
            }
		}
	}
    
    STW_stormwind_centralize_elwynn = { 
		icon = mission_lumbermill
        position = 2
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_calm_subjects } 
        
		trigger = {
            region_elwynn_forest = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
		}
        provinces_to_highlight = {
            region = region_elwynn_forest
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_centralized_elwynn"
				duration = -1
			}
		}
	}
    
    STW_stormwind_unite_azerothian_lands = { 
		icon = mission_scroll
        position = 3
		required_missions = { STW_stormwind_centralize_elwynn } 
        
		trigger = {
            calc_true_if = {
				region_westfall = {
					type = all
					country_or_non_sovereign_subject_holds = ROOT
				}
				region_duskwood = {
					type = all
					country_or_non_sovereign_subject_holds = ROOT
				}
				region_redridge_mountains = {
					type = all
					country_or_non_sovereign_subject_holds = ROOT
				}
				region_deadwind_pass = {
					type = all
					country_or_non_sovereign_subject_holds = ROOT
				}
				amount = 50
			}
		}
        provinces_to_highlight = {
            OR = {
                region = region_westfall
                region = region_duskwood
                region = region_redridge_mountains
                region = region_deadwind_pass
            }
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_unity_of_stormwind"
				duration = -1
			}
		}
	}
    
    STW_stormwind_crush_the_gnoll_threat = { 
		icon = mission_sparring_equipment
        position = 4
		required_missions = { STW_stormwind_unite_azerothian_lands } 
        
		trigger = {
            area_lakeshire = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
                NOT = { culture_group = culture_group_gnoll }
			}
            area_lakeshire_highway = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
                NOT = { culture_group = culture_group_gnoll }
			}
            area_redridge_canyons = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
                NOT = { culture_group = culture_group_gnoll }
			}
		}
        provinces_to_highlight = {
            culture_group = culture_group_gnoll
            OR = {
                area = area_lakeshire
                area = area_lakeshire_highway
                area = area_redridge_canyons
            }
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_gnoll_purge"
				duration = -1
			}
		}
	}
}

#STW_stormwind_column_3 = {
	slot = 3
	generic = no
	ai = yes
    has_country_shield = yes
    
	potential = {
		tag = STW
		has_country_flag = stormwind_one_finished
	}
    
    STW_stormwind_secure_duskwood_banks = { 
		icon = mission_secretive_plot
        position = 2
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_calm_subjects } 
        
		trigger = {
            area_the_darkened_banks = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
		}
        provinces_to_highlight = {
            area = area_the_darkened_banks
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_darkshire_trade"
				duration = -1
			}
		}
	}
    
    STW_stormwind_root_out_kobolds = { 
		icon = mission_mining
        position = 4
		required_missions = { STW_stormwind_unite_azerothian_lands } 
        
		trigger = {
            region_westfall = {
				type = all
				NOT = { culture_group = culture_group_kobold }
			}
            region_elwynn_forest = {
				type = all
				NOT = { culture_group = culture_group_kobold }
			}
            region_duskwood = {
				type = all
				NOT = { culture_group = culture_group_kobold }
			}
            region_redridge_mountains = {
				type = all
				NOT = { culture_group = culture_group_kobold }
			}
		}
        provinces_to_highlight = {
            culture_group = culture_group_kobold
            OR = {
                region = region_westfall
                region = region_elwynn_forest
                region = region_duskwood
                region = region_redridge_mountains
            }
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_kobold_purge"
				duration = -1
			}
		}
	}
}

#STW_stormwind_column_4 = { 
	slot = 4
	generic = no
	ai = yes
    has_country_shield = yes
    
	potential = {
		tag = STW
		has_country_flag = stormwind_one_finished
	} 
    
    STW_stormwind_prepare_for_invasion = { 
		icon = mission_tools
        position = 1
        completed_by = 592.1.1 # First War
        
		required_missions = {  } 
        
		trigger = {
            OR = {
                exists = U03
                any_country = {
                    has_country_flag = orcish_horde_primary_nation
                }
            }
            army_size_percentage = 0.9
		}
		effect = { 
			add_country_modifier = {
				name = "mission_prepared_for_invasion"
				duration = -1
			}
		}
	}
    
    STW_stormwind_establish_forward_outpost = { 
		icon = mission_headquarters
        position = 2
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_prepare_for_invasion } 
        
		trigger = {
            owns_core_province = 864
		}
        provinces_to_highlight = {
            province_id = 864
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_swamp_base"
				duration = -1
			}
		}
	}
    
     STW_stormwind_push_back_the_orcish_horde = { 
		icon = mission_paladin_empowered_seals_truth
        position = 3
        completed_by = 592.1.1 # First War
        
		required_missions = { 
            STW_stormwind_establish_forward_outpost 
        } 
        
		trigger = {
            OR = {
                war_with = U03
                any_country = {
                    war_with = ROOT
                    has_country_flag = orcish_horde_primary_nation
                }
            }
            1035 = {
                controlled_by = ROOT
            }
		}
        provinces_to_highlight = {
            province_id = 1035
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_heroes_of_the_first_war"
				duration = -1
			}
            
            country_event = { id = first_war.6 }
		}
	}
}

#STW_stormwind_column_5 = {
	slot = 5
	generic = no
	ai = yes
    has_country_shield = yes
    
	potential = {
		tag = STW
		has_country_flag = stormwind_one_finished
	} 
    
    STW_stormwind_cut_down_the_gurubashi = { 
		icon = mission_troll_male
        position = 2
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_prepare_for_invasion } 
        
		trigger = {
            owns_core_province = 601
            owns_core_province = 1997
		}
        provinces_to_highlight = {
            OR = {
                province_id = 601
                province_id = 1997
			}
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_gurubashi_neutralized"
				duration = -1
			}
		}
	}
    
    STW_stormwind_secure_the_swamp = { 
		icon = mission_camp_flag
        position = 3
        completed_by = 592.1.1 # First War
        
		required_missions = { STW_stormwind_establish_forward_outpost } 
        
		trigger = {
            area_crackling_banks = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
            area_stagalbog = {
				type = all
				country_or_non_sovereign_subject_holds = ROOT
			}
		}
        provinces_to_highlight = {
            OR = {
				area = area_crackling_banks
				area = area_stagalbog
			}
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
		effect = { 
			add_country_modifier = {
				name = "mission_secured_the_swamp"
				duration = -1
			}
		}
	}
}