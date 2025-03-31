import json
import os
import pandas as pd
from pathlib import Path

# In a real application, this would interact with a database
# For this prototype, we'll simulate data loading from JSON files

def _get_data_dir():
    """Get the path to the data directory."""
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    # Go up one level to the app directory
    app_dir = current_dir.parent
    # Get the data directory
    data_dir = app_dir / "data"
    return data_dir

def load_civilizations():
    """Load civilization data."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data
    
    # Check if we have a civilizations.json file
    data_dir = _get_data_dir()
    civ_file = data_dir / "civilizations.json"
    
    if civ_file.exists():
        # Load from file
        with open(civ_file, 'r') as f:
            return json.load(f)
    
    # If no file exists, return sample data
    return [
        {
            "id": 1,
            "name": "Franks",
            "display_name": "Franks (Cavalry)",
            "icon_path": None,
            "specialty": ["Cavalry", "Economy"],
            "unique_units": ["Throwing Axeman"],
            "unique_techs": [
                {"name": "Bearded Axe", "age": "Castle", "effect": "Throwing Axeman +1 range"},
                {"name": "Chivalry", "age": "Imperial", "effect": "Stable units created 40% faster"}
            ],
            "civilization_bonuses": [
                "Farm upgrades are free",
                "Foragers work 25% faster",
                "Knights have +20% HP",
                "Castles cost -25%"
            ],
            "team_bonus": "Knights +2 line of sight",
            "economy_rating": {"food": 9, "wood": 6, "gold": 6, "stone": 5},
            "military_rating": {"cavalry": 10, "infantry": 5, "archers": 4, "siege": 6, "navy": 4, "monks": 4},
            "tech_tree_limitations": ["Arbalester", "Heavy Cavalry Archer", "Elite Elephant Archer", "Camel Rider", "Ring Archer Armor", "Parthian Tactics"],
            "optimal_ages": ["Castle Age", "Imperial Age"],
            "dlc": "Base Game",
            "primary_specialty": "Cavalry"
        },
        {
            "id": 2,
            "name": "Britons",
            "display_name": "Britons (Archers)",
            "icon_path": None,
            "specialty": ["Archers", "Economy"],
            "unique_units": ["Longbowman"],
            "unique_techs": [
                {"name": "Yeomen", "age": "Castle", "effect": "Foot archers +1 range, towers +2 attack"},
                {"name": "Warwolf", "age": "Imperial", "effect": "Trebuchets deal splash damage"}
            ],
            "civilization_bonuses": [
                "Town Centers cost -50% wood starting in Castle Age",
                "Foot archers (except skirmishers) +1 range in Castle Age, +2 in Imperial Age",
                "Shepherds work 25% faster"
            ],
            "team_bonus": "Archery Ranges work 20% faster",
            "economy_rating": {"food": 7, "wood": 8, "gold": 6, "stone": 5},
            "military_rating": {"cavalry": 4, "infantry": 5, "archers": 10, "siege": 7, "navy": 6, "monks": 4},
            "tech_tree_limitations": ["Camel Rider", "Hussar", "Paladin", "Hand Cannoneer", "Bombard Cannon", "Redemption", "Atonement", "Faith"],
            "optimal_ages": ["Feudal Age", "Imperial Age"],
            "dlc": "Base Game",
            "primary_specialty": "Archers"
        },
        {
            "id": 3,
            "name": "Aztecs",
            "display_name": "Aztecs (Infantry & Monks)",
            "icon_path": None,
            "specialty": ["Infantry", "Monks", "Economy"],
            "unique_units": ["Jaguar Warrior"],
            "unique_techs": [
                {"name": "Atlatl", "age": "Castle", "effect": "Skirmishers +1 attack, +1 range"},
                {"name": "Garland Wars", "age": "Imperial", "effect": "Infantry +4 attack"}
            ],
            "civilization_bonuses": [
                "Villagers carry +5",
                "Military units created 15% faster",
                "Monks +5 HP for each monastery technology",
                "Start with +50 gold"
            ],
            "team_bonus": "Relics generate +33% gold",
            "economy_rating": {"food": 7, "wood": 7, "gold": 8, "stone": 6},
            "military_rating": {"cavalry": 0, "infantry": 9, "archers": 7, "siege": 6, "navy": 6, "monks": 10},
            "tech_tree_limitations": ["All cavalry units", "Hand Cannoneer", "Bombard Cannon", "Keep", "Bombard Tower"],
            "optimal_ages": ["Feudal Age", "Castle Age"],
            "dlc": "The Conquerors",
            "primary_specialty": "Infantry"
        }
    ]

def load_featured_build_orders():
    """Load featured build orders."""
    # In a real app, this would query a database for featured/recommended builds
    # For this prototype, we'll return sample data
    
    # Check if we have a build_orders.json file
    data_dir = _get_data_dir()
    build_file = data_dir / "build_orders.json"
    
    if build_file.exists():
        # Load from file
        with open(build_file, 'r') as f:
            builds = json.load(f)
            # Return only featured builds (in a real app, this would be tagged in the database)
            return [b for b in builds if b.get("featured", False)]
    
    # If no file exists, return sample data
    return [
        {
            "id": 1,
            "name": "21 Pop Scout Rush",
            "type": "Feudal Rush",
            "primary_goal": "Early pressure",
            "description": "A fast Feudal Age upgrade followed by Scout Cavalry production to raid the enemy economy and disrupt their build-up.",
            "difficulty": "Intermediate",
            "creator": "St4rk",
            "meta_relevance": 8,
            "execution_time": 10,
            "suitable_maps": ["Arabia", "Gold Rush", "Four Lakes"],
            "strong_against": ["Slow boom strategies", "Archer civilizations"],
            "weak_against": ["Full wall strategies", "Fast Men-at-Arms"],
            "ideal_civilizations": [1, 5, 7],  # IDs for Franks, Magyars, Huns
            "ideal_civilizations_names": ["Franks", "Magyars", "Huns"],
            "compatible_civilizations": [1, 5, 7, 9, 14],
            "incompatible_civilizations": [3, 4, 18],
            "featured": True
        },
        {
            "id": 2,
            "name": "Archer Rush (23 Pop)",
            "type": "Feudal Rush",
            "primary_goal": "Map control",
            "description": "This build focuses on quick Feudal Age advancement and production of Archers to gain map control and pressure the opponent.",
            "difficulty": "Intermediate",
            "creator": "Hera",
            "meta_relevance": 9,
            "execution_time": 12,
            "suitable_maps": ["Arabia", "Highland", "Gold Rush"],
            "strong_against": ["Scout rushes", "Forward strategies"],
            "weak_against": ["Skirmisher defense", "Fast Castle into Knights"],
            "ideal_civilizations": [2, 8, 11],  # IDs for Britons, Ethiopians, Mayans
            "ideal_civilizations_names": ["Britons", "Ethiopians", "Mayans"],
            "compatible_civilizations": [2, 8, 11, 21, 26],
            "incompatible_civilizations": [1, 5, 12],
            "featured": True
        },
        {
            "id": 3,
            "name": "Fast Castle into Knights",
            "type": "Fast Castle",
            "primary_goal": "Castle Age power spike",
            "description": "Skip Feudal Age aggression and go straight to Castle Age to produce powerful Knights for a mid-game timing attack.",
            "difficulty": "Beginner",
            "creator": "TheViper",
            "meta_relevance": 7,
            "execution_time": 16,
            "suitable_maps": ["Arena", "Black Forest", "Fortress"],
            "strong_against": ["Archer rushes", "Boom strategies"],
            "weak_against": ["Early pressure", "Camel civilizations"],
            "ideal_civilizations": [1, 6, 15],  # IDs for Franks, Berbers, Lithuanians
            "ideal_civilizations_names": ["Franks", "Berbers", "Lithuanians"],
            "compatible_civilizations": [1, 6, 15, 19, 31],
            "incompatible_civilizations": [3, 8, 17],
            "featured": True
        }
    ]

def load_build_orders():
    """Load all build orders."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data
    
    # Check if we have a build_orders.json file
    data_dir = _get_data_dir()
    build_file = data_dir / "build_orders.json"
    
    if build_file.exists():
        # Load from file
        with open(build_file, 'r') as f:
            return json.load(f)
    
    # If no file exists, return sample data
    # This would be the same as featured builds plus more
    featured = load_featured_build_orders()
    return featured + [
        {
            "id": 4,
            "name": "Men-at-Arms into Archers",
            "type": "Feudal Rush",
            "primary_goal": "Early aggression",
            "description": "Open with Men-at-Arms to apply early pressure, then transition into Archers for sustained damage.",
            "difficulty": "Advanced",
            "creator": "TaToH",
            "meta_relevance": 8,
            "execution_time": 13,
            "suitable_maps": ["Arabia", "Acropolis", "Serengeti"],
            "strong_against": ["Scout rushes", "Greedy builds"],
            "weak_against": ["Tower defense", "Skirmisher defense"],
            "ideal_civilizations": [3, 9, 17],  # IDs for Aztecs, Vikings, Japanese
            "ideal_civilizations_names": ["Aztecs", "Vikings", "Japanese"],
            "compatible_civilizations": [3, 9, 17, 22, 28],
            "incompatible_civilizations": [7, 10, 16],
            "featured": False
        },
        {
            "id": 5,
            "name": "Tower Rush",
            "type": "Feudal Rush",
            "primary_goal": "Resource denial",
            "description": "Advance to Feudal Age and build forward towers to deny key resources and apply constant pressure.",
            "difficulty": "Expert",
            "creator": "Liereyy",
            "meta_relevance": 6,
            "execution_time": 10,
            "suitable_maps": ["Arabia", "Gold Rush", "Acropolis"],
            "strong_against": ["Greedy builds", "Immobile strategies"],
            "weak_against": ["Early aggression", "Multiple TCs"],
            "ideal_civilizations": [12, 24, 30],  # IDs for Koreans, Incas, Spanish
            "ideal_civilizations_names": ["Koreans", "Incas", "Spanish"],
            "compatible_civilizations": [12, 24, 30, 32, 35],
            "incompatible_civilizations": [2, 13, 27],
            "featured": False
        }
    ]

def load_maps():
    """Load map data."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data
    
    # Check if we have a maps.json file
    data_dir = _get_data_dir()
    maps_file = data_dir / "maps.json"
    
    if maps_file.exists():
        # Load from file
        with open(maps_file, 'r') as f:
            return json.load(f)
    
    # If no file exists, return sample data
    return [
        {
            "id": 1,
            "name": "Arabia",
            "type": "Open",
            "size_options": ["Tiny", "Small", "Medium", "Large", "Huge", "Gigantic", "Ludicrous"],
            "resources": {
                "food": "Medium",
                "wood": "Medium",
                "gold": "Medium",
                "stone": "Medium"
            },
            "starting_resources": {
                "wood": 200,
                "food": 200,
                "gold": 100,
                "stone": 200
            },
            "characteristics": [
                "Few forests",
                "Open map",
                "Standard resources",
                "Aggressive early game",
                "Standard starting position"
            ],
            "strong_civilizations": [1, 2, 3, 5, 8],  # IDs for top 5 civs
            "strong_civilizations_names": ["Franks", "Britons", "Aztecs", "Magyars", "Ethiopians"],
            "weak_civilizations": [10, 13, 22, 27, 33],  # IDs for bottom 5 civs
            "weak_civilizations_names": ["Persians", "Portuguese", "Burmese", "Vietnamese", "Italians"],
            "common_strategies": [
                "Scout Rush",
                "Archer Rush",
                "Men-at-Arms into Archers",
                "Drush Fast Castle",
                "Tower Rush"
            ],
            "image_path": None
        },
        {
            "id": 2,
            "name": "Arena",
            "type": "Closed",
            "size_options": ["Tiny", "Small", "Medium", "Large", "Huge", "Gigantic", "Ludicrous"],
            "resources": {
                "food": "Medium",
                "wood": "High",
                "gold": "Medium",
                "stone": "Medium"
            },
            "starting_resources": {
                "wood": 200,
                "food": 200,
                "gold": 100,
                "stone": 200
            },
            "characteristics": [
                "Fully walled starting position",
                "Single entrance",
                "Many forests",
                "Relaxed early game",
                "Important late-game resource control"
            ],
            "strong_civilizations": [3, 9, 12, 15, 18],  # IDs for top 5 civs
            "strong_civilizations_names": ["Aztecs", "Vikings", "Koreans", "Lithuanians", "Teutons"],
            "weak_civilizations": [4, 7, 11, 25, 31],  # IDs for bottom 5 civs
            "weak_civilizations_names": ["Huns", "Mayans", "Mongols", "Cumans", "Bulgarians"],
            "common_strategies": [
                "Fast Castle",
                "Boom into Imperial",
                "Castle Drop",
                "Monk Rush",
                "Siege Civilization Push"
            ],
            "image_path": None
        },
        {
            "id": 3,
            "name": "Islands",
            "type": "Water",
            "size_options": ["Tiny", "Small", "Medium", "Large", "Huge", "Gigantic", "Ludicrous"],
            "resources": {
                "food": "High",
                "wood": "Medium",
                "gold": "Medium",
                "stone": "Low"
            },
            "starting_resources": {
                "wood": 200,
                "food": 200,
                "gold": 100,
                "stone": 200
            },
            "characteristics": [
                "Players start on separate islands",
                "Water dominance is crucial",
                "Fish abundance",
                "Late-game resource scarcity",
                "Limited land area"
            ],
            "strong_civilizations": [10, 13, 19, 23, 33],  # IDs for top 5 civs
            "strong_civilizations_names": ["Persians", "Portuguese", "Italians", "Malay", "Vikings"],
            "weak_civilizations": [3, 6, 17, 28, 35],  # IDs for bottom 5 civs
            "weak_civilizations_names": ["Aztecs", "Berbers", "Japanese", "Khmer", "Spanish"],
            "common_strategies": [
                "Fishing Boom",
                "Galley Rush",
                "Fast Fire Ship",
                "Transport Landing",
                "Defensive Boom"
            ],
            "image_path": None
        }
    ]

def load_map_specific_strategies(map_id):
    """Load strategies specific to a map."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data based on the map ID
    
    # Sample strategies for Arabia (map_id = 1)
    if map_id == 1:
        return [
            {
                "name": "Early Aggression",
                "type": "Feudal Rush",
                "description": "Focus on early pressure with Scouts or Archers to disrupt the opponent's economy.",
                "key_points": [
                    "Advance to Feudal Age around 21-23 population",
                    "Scout the enemy early to determine their strategy",
                    "Focus on map control and disrupting the opponent's economy",
                    "Transition to Castle Age around 30-35 population"
                ],
                "suitable_civilizations": ["Franks", "Britons", "Mayans", "Ethiopians", "Magyars"]
            },
            {
                "name": "Drush FC",
                "type": "Fast Castle",
                "description": "Use a Dark Age Militia rush to buy time for a Fast Castle build.",
                "key_points": [
                    "Create 3 Militia in Dark Age to harass",
                    "Focus on getting to Castle Age around 27-28 population",
                    "Scout the enemy to ensure your safety",
                    "Transition into Knights or Crossbowmen based on civilization"
                ],
                "suitable_civilizations": ["Aztecs", "Malay", "Byzantines", "Malians", "Lithuanians"]
            },
            {
                "name": "Archer Dominance",
                "type": "Sustained Pressure",
                "description": "Focus on massing Archers in Feudal Age and maintaining pressure through Castle Age.",
                "key_points": [
                    "Advance to Feudal Age around 22-24 population",
                    "Mass Archers and add Skirmishers if needed",
                    "Upgrade to Crossbowmen in Castle Age",
                    "Control key areas and deny resources"
                ],
                "suitable_civilizations": ["Britons", "Mayans", "Ethiopians", "Vietnamese", "Chinese"]
            }
        ]
    
    # Sample strategies for Arena (map_id = 2)
    elif map_id == 2:
        return [
            {
                "name": "Fast Imperial",
                "type": "Boom",
                "description": "Boom economically and advance to Imperial Age as fast as possible for a powerful timing attack.",
                "key_points": [
                    "Advance to Castle Age around 27-28 population",
                    "Add 3-4 Town Centers and boom",
                    "Research key economy upgrades",
                    "Advance to Imperial Age around 34-36 minutes",
                    "Push with powerful Imperial Age units"
                ],
                "suitable_civilizations": ["Turks", "Teutons", "Byzantines", "Slavs", "Spanish"]
            },
            {
                "name": "Monk Rush",
                "type": "Castle Age Pressure",
                "description": "Advance to Castle Age quickly and pressure with Monks to collect relics and disrupt the opponent.",
                "key_points": [
                    "Advance to Castle Age around 26-27 population",
                    "Build a Monastery and produce Monks",
                    "Research Monastery technologies",
                    "Collect relics and convert enemy units",
                    "Support with defensive units"
                ],
                "suitable_civilizations": ["Aztecs", "Burmese", "Byzantines", "Lithuanians", "Spanish"]
            },
            {
                "name": "Castle Drop",
                "type": "Aggressive Push",
                "description": "Advance to Castle Age and immediately build a forward Castle to apply pressure.",
                "key_points": [
                    "Collect stone in Feudal Age",
                    "Advance to Castle Age around 27-29 population",
                    "Build a forward Castle near the enemy walls",
                    "Produce unique units or apply pressure",
                    "Follow up with siege or economy"
                ],
                "suitable_civilizations": ["Koreans", "Spanish", "Turks", "Franks", "Incas"]
            }
        ]
    
    # Sample strategies for Islands (map_id = 3)
    elif map_id == 3:
        return [
            {
                "name": "Fishing Boom",
                "type": "Economic",
                "description": "Focus on building Fishing Ships early to establish a strong economy.",
                "key_points": [
                    "Build a Dock immediately",
                    "Create 10-15 Fishing Ships",
                    "Advance to Feudal Age around 25-28 population",
                    "Prepare for naval battles",
                    "Secure key water areas"
                ],
                "suitable_civilizations": ["Japanese", "Persians", "Malay", "Vikings", "Italians"]
            },
            {
                "name": "Fire Galley Rush",
                "type": "Feudal Rush",
                "description": "Advance to Feudal Age quickly and produce Fire Galleys to control the water.",
                "key_points": [
                    "Build a Dock and a few Fishing Ships",
                    "Advance to Feudal Age around 22-23 population",
                    "Build 2-3 Docks and produce Fire Galleys",
                    "Control key water areas",
                    "Deny enemy fishing and water access"
                ],
                "suitable_civilizations": ["Persians", "Vikings", "Portuguese", "Byzantines", "Italians"]
            },
            {
                "name": "Transport Landing",
                "type": "Aggressive",
                "description": "Prepare a land army and transport to the enemy island for a surprise attack.",
                "key_points": [
                    "Build a Dock and gain some water control",
                    "Prepare military units in Feudal or Castle Age",
                    "Build Transport Ships",
                    "Land on the enemy island in an undefended area",
                    "Set up a forward base and apply pressure"
                ],
                "suitable_civilizations": ["Persians", "Vikings", "Malians", "Spanish", "Magyars"]
            }
        ]
    
    # Default: return empty list if map_id doesn't match
    return []

def load_matchup_data(civ1_id, civ2_id):
    """Load matchup data between two civilizations."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data based on the civilization IDs
    
    # Check if we have a civilization_matchups.csv file
    data_dir = _get_data_dir()
    matchup_file = data_dir / "civilization_matchups.csv"
    
    if matchup_file.exists():
        # Load from file
        df = pd.read_csv(matchup_file)
        
        # Find the specific matchup
        matchup = df[(df["civ1_id"] == civ1_id) & (df["civ2_id"] == civ2_id)]
        
        if not matchup.empty:
            row = matchup.iloc[0]
            return {
                "civ1_id": int(row["civ1_id"]),
                "civ2_id": int(row["civ2_id"]),
                "win_rate": float(row["win_rate"]),
                "sample_size": int(row["sample_size"]),
                "advantage_level": row["advantage_level"],
                "key_factors": json.loads(row["key_factors"]) if isinstance(row["key_factors"], str) else row["key_factors"],
                "counter_strategies": json.loads(row["counter_strategies"]) if isinstance(row["counter_strategies"], str) else row["counter_strategies"],
                "ideal_build_orders": json.loads(row["ideal_build_orders"]) if isinstance(row["ideal_build_orders"], str) else row["ideal_build_orders"]
            }
    
    # If no file exists or matchup not found, return sample data
    
    # Franks (1) vs Britons (2)
    if civ1_id == 1 and civ2_id == 2:
        return {
            "civ1_id": 1,
            "civ2_id": 2,
            "win_rate": 48.5,
            "sample_size": 1250,
            "advantage_level": "Slight Disadvantage",
            "key_factors": [
                "Britons' superior archers counter Franks' cavalry",
                "Franks need to force close engagements",
                "Britons have a stronger late game"
            ],
            "counter_strategies": [
                "Use Skirmishers to counter archers",
                "Build Siege Workshops for Scorpions",
                "Push aggressively in Castle Age before Britons mass Longbowmen",
                "Raid with fast Knights to disrupt economy"
            ],
            "ideal_build_orders": [1, 3]  # IDs of recommended build orders
        }
    
    # Franks (1) vs Aztecs (3)
    elif civ1_id == 1 and civ2_id == 3:
        return {
            "civ1_id": 1,
            "civ2_id": 3,
            "win_rate": 53.2,
            "sample_size": 980,
            "advantage_level": "Slight Advantage",
            "key_factors": [
                "Franks' cavalry counters Aztecs' infantry",
                "Aztecs lack cavalry counters in late game",
                "Franks have stronger late game"
            ],
            "counter_strategies": [
                "Push early with Knights before Aztecs can mass Monks",
                "Build multiple Stables to overwhelm with numbers",
                "Avoid Aztec Pikemen and Monks",
                "Use Throwing Axemen against infantry"
            ],
            "ideal_build_orders": [1, 3]  # IDs of recommended build orders
        }
    
    # Britons (2) vs Aztecs (3)
    elif civ1_id == 2 and civ2_id == 3:
        return {
            "civ1_id": 2,
            "civ2_id": 3,
            "win_rate": 51.8,
            "sample_size": 1050,
            "advantage_level": "Even",
            "key_factors": [
                "Both civilizations have strong archer plays",
                "Aztecs have stronger early economy",
                "Britons have superior late game archers"
            ],
            "counter_strategies": [
                "Focus on Crossbowmen and Longbowmen",
                "Use range advantage to kite Aztec units",
                "Defend against early aggression",
                "Establish map control with superior archer range"
            ],
            "ideal_build_orders": [2, 4]  # IDs of recommended build orders
        }
    
    # Default for any other matchup
    return {
        "civ1_id": civ1_id,
        "civ2_id": civ2_id,
        "win_rate": 50.0,
        "sample_size": 500,
        "advantage_level": "Even",
        "key_factors": [
            "Both civilizations have balanced strengths and weaknesses",
            "Outcome depends heavily on player skill and map generation",
            "No significant matchup advantages"
        ],
        "counter_strategies": [
            "Play to your civilization's strengths",
            "Scout early to determine opponent's strategy",
            "Adapt based on map and resources"
        ],
        "ideal_build_orders": [1, 2, 3]  # IDs of generic build orders
    }

def load_civilization_statistics(elo_range=None, patch_version=None, map_type=None):
    """Load civilization statistics with optional filters."""
    # In a real app, this would query a database with filters
    # For this prototype, we'll return sample data
    
    # This would be affected by the filters in a real app
    return [
        {
            "id": 1,
            "name": "Franks",
            "win_rate": 54.2,
            "pick_rate": 8.7,
            "primary_specialty": "Cavalry"
        },
        {
            "id": 2,
            "name": "Britons",
            "win_rate": 52.8,
            "pick_rate": 6.5,
            "primary_specialty": "Archers"
        },
        {
            "id": 3,
            "name": "Aztecs",
            "win_rate": 51.9,
            "pick_rate": 5.8,
            "primary_specialty": "Infantry"
        },
        {
            "id": 4,
            "name": "Huns",
            "win_rate": 51.2,
            "pick_rate": 4.2,
            "primary_specialty": "Cavalry"
        },
        {
            "id": 5,
            "name": "Magyars",
            "win_rate": 50.8,
            "pick_rate": 3.9,
            "primary_specialty": "Cavalry"
        },
        {
            "id": 6,
            "name": "Berbers",
            "win_rate": 50.5,
            "pick_rate": 2.8,
            "primary_specialty": "Cavalry"
        },
        {
            "id": 7,
            "name": "Chinese",
            "win_rate": 50.2,
            "pick_rate": 4.5,
            "primary_specialty": "Archers"
        },
        {
            "id": 8,
            "name": "Ethiopians",
            "win_rate": 49.8,
            "pick_rate": 3.2,
            "primary_specialty": "Archers"
        },
        {
            "id": 9,
            "name": "Vikings",
            "win_rate": 49.6,
            "pick_rate": 4.1,
            "primary_specialty": "Infantry"
        },
        {
            "id": 10,
            "name": "Persians",
            "win_rate": 49.3,
            "pick_rate": 2.7,
            "primary_specialty": "Cavalry"
        }
    ]

def load_build_order_statistics():
    """Load build order success statistics."""
    # In a real app, this would query a database
    # For this prototype, we'll return sample data
    return [
        {
            "id": 1,
            "name": "21 Pop Scout Rush",
            "success_rate": 68.5,
            "popularity": 12.4,
            "type": "Feudal Rush",
            "difficulty": "Intermediate"
        },
        {
            "id": 2,
            "name": "Archer Rush (23 Pop)",
            "success_rate": 65.2,
            "popularity": 15.8,
            "type": "Feudal Rush",
            "difficulty": "Intermediate"
        },
        {
            "id": 3,
            "name": "Fast Castle into Knights",
            "success_rate": 62.7,
            "popularity": 18.6,
            "type": "Fast Castle",
            "difficulty": "Beginner"
        },
        {
            "id": 4,
            "name": "Men-at-Arms into Archers",
            "success_rate": 61.8,
            "popularity": 8.9,
            "type": "Feudal Rush",
            "difficulty": "Advanced"
        },
        {
            "id": 5,
            "name": "Tower Rush",
            "success_rate": 58.4,
            "popularity": 5.2,
            "type": "Feudal Rush",
            "difficulty": "Expert"
        },
        {
            "id": 6,
            "name": "Fast Imperial",
            "success_rate": 57.2,
            "popularity": 7.3,
            "type": "Boom",
            "difficulty": "Advanced"
        },
        {
            "id": 7,
            "name": "Drush Fast Castle",
            "success_rate": 64.1,
            "popularity": 9.2,
            "type": "Fast Castle",
            "difficulty": "Advanced"
        },
        {
            "id": 8,
            "name": "Monk Rush",
            "success_rate": 53.8,
            "popularity": 3.4,
            "type": "Castle Age",
            "difficulty": "Expert"
        },
        {
            "id": 9,
            "name": "Fishing Boom",
            "success_rate": 67.2,
            "popularity": 6.8,
            "type": "Economic",
            "difficulty": "Beginner"
        },
        {
            "id": 10,
            "name": "Fire Galley Rush",
            "success_rate": 59.6,
            "popularity": 4.7,
            "type": "Feudal Rush",
            "difficulty": "Intermediate"
        }
    ] 