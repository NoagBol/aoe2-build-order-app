import os
import json
from pathlib import Path

def create_directory_structure():
    """Create the necessary directory structure for the application."""
    app_root = Path(__file__).parent
    
    # Create directories
    directories = [
        'assets/data',
        'assets/images',
        'assets/images/civilizations',
        'assets/images/maps',
        'assets/images/units',
        'assets/images/icons',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(app_root / directory, exist_ok=True)
    
    print("Directory structure created successfully.")

def create_sample_data():
    """Create sample data files if they don't exist."""
    app_root = Path(__file__).parent
    
    # Sample civilizations data
    civilizations_data = {
        "civilizations": [
            {
                "id": "franks",
                "name": "Franks",
                "expansion": "Age of Kings",
                "specialty": ["Cavalry", "Economy"],
                "unique_units": ["Throwing Axeman"],
                "unique_techs": ["Bearded Axe", "Chivalry"],
                "team_bonus": "Knights +2 line of sight",
                "bonuses": [
                    "Farm upgrades free",
                    "Knights +20% HP",
                    "Castles cost -25%",
                    "Foragers work +25% faster"
                ],
                "ratings": {
                    "infantry": 3,
                    "cavalry": 5,
                    "archers": 1,
                    "siege": 3, 
                    "navy": 1,
                    "monks": 2,
                    "defense": 3,
                    "economy": 4
                },
                "dlc": None,
                "icon_path": "assets/images/civilizations/franks.png"
            },
            {
                "id": "britons",
                "name": "Britons",
                "expansion": "Age of Kings",
                "specialty": ["Archers", "Defense"],
                "unique_units": ["Longbowman"],
                "unique_techs": ["Yeomen", "Warwolf"],
                "team_bonus": "Archery Ranges work 20% faster",
                "bonuses": [
                    "Town Centers cost -50% wood starting in Castle Age",
                    "Foot archers (except Skirmishers) +1/+2 range in Castle/Imperial Age",
                    "Shepherds work 25% faster"
                ],
                "ratings": {
                    "infantry": 3,
                    "cavalry": 2,
                    "archers": 5,
                    "siege": 4,
                    "navy": 3,
                    "monks": 2,
                    "defense": 4,
                    "economy": 3
                },
                "dlc": None,
                "icon_path": "assets/images/civilizations/britons.png"
            },
            {
                "id": "aztecs",
                "name": "Aztecs",
                "expansion": "The Conquerors",
                "specialty": ["Infantry", "Monks", "Economy"],
                "unique_units": ["Jaguar Warrior"],
                "unique_techs": ["Atlatl", "Garland Wars"],
                "team_bonus": "Relics generate +33% gold",
                "bonuses": [
                    "Villagers carry +5",
                    "Military units created 15% faster",
                    "Start with +50 gold",
                    "Monk +5 HP for each monastery technology",
                    "Loom free"
                ],
                "ratings": {
                    "infantry": 5,
                    "cavalry": 0,
                    "archers": 3,
                    "siege": 3,
                    "navy": 2,
                    "monks": 5,
                    "defense": 3,
                    "economy": 4
                },
                "dlc": None,
                "icon_path": "assets/images/civilizations/aztecs.png"
            }
        ]
    }
    
    # Sample build orders data
    build_orders_data = {
        "build_orders": [
            {
                "id": "franks_fast_castle",
                "name": "Franks Fast Castle",
                "description": "Standard Fast Castle into Knights",
                "type": "Fast Castle",
                "difficulty": "Medium",
                "primary_goal": "Reach Castle Age quickly and mass Knights",
                "execution_time": 1020,  # 17:00 minutes
                "creator": "St4rk",
                "meta_relevance": "High",
                "suitable_maps": ["Arabia", "Hideout", "Arena"],
                "ideal_civilizations": ["Franks", "Lithuanians", "Berbers"],
                "matchups": {
                    "good_against": ["Britons", "Mayans", "Vietnamese"],
                    "bad_against": ["Byzantines", "Camels", "Halberdiers"]
                },
                "steps": [
                    {
                        "population": 6,
                        "age": "dark",
                        "time": 0,
                        "instruction": "Send first 6 villagers to sheep"
                    },
                    {
                        "population": 7,
                        "age": "dark",
                        "time": 25,
                        "instruction": "Build house with 7th villager, then send to sheep"
                    },
                    {
                        "population": 10,
                        "age": "dark",
                        "time": 120,
                        "instruction": "Build lumber camp with 10th villager, then 10-13 to wood"
                    },
                    {
                        "population": 14,
                        "age": "dark",
                        "time": 210,
                        "instruction": "Send 14-16 to berries, build mill"
                    },
                    {
                        "population": 17,
                        "age": "dark",
                        "time": 280,
                        "instruction": "Send 17-19 to gold, build mining camp"
                    },
                    {
                        "population": 20,
                        "age": "dark",
                        "time": 370,
                        "instruction": "20th villager builds house, then to gold"
                    },
                    {
                        "population": 22,
                        "age": "dark",
                        "time": 420,
                        "instruction": "Click up to Feudal Age"
                    },
                    {
                        "population": 24,
                        "age": "dark",
                        "time": 480,
                        "instruction": "Send 21-24 to wood"
                    },
                    {
                        "population": 26,
                        "age": "feudal",
                        "time": 600,
                        "instruction": "Reach Feudal Age. Build market and blacksmith."
                    },
                    {
                        "population": 28,
                        "age": "feudal",
                        "time": 680,
                        "instruction": "Send 25-28 to food (farms)"
                    },
                    {
                        "population": 29,
                        "age": "feudal",
                        "time": 720,
                        "instruction": "Click up to Castle Age"
                    },
                    {
                        "population": 30,
                        "age": "feudal",
                        "time": 750,
                        "instruction": "Build 2 more farms"
                    },
                    {
                        "population": 32,
                        "age": "castle",
                        "time": 900,
                        "instruction": "Reach Castle Age. Build 2 stables, start creating knights"
                    },
                    {
                        "population": 35,
                        "age": "castle",
                        "time": 960,
                        "instruction": "Research Bloodlines and add more farms"
                    },
                    {
                        "population": 40,
                        "age": "castle",
                        "time": 1020,
                        "instruction": "Add a third stable and continue knight production"
                    }
                ],
                "villager_assignments": [
                    {"time": 0, "food": 6, "wood": 0, "gold": 0, "stone": 0},
                    {"time": 120, "food": 9, "wood": 3, "gold": 0, "stone": 0},
                    {"time": 210, "food": 12, "wood": 3, "gold": 0, "stone": 0},
                    {"time": 280, "food": 12, "wood": 3, "gold": 3, "stone": 0},
                    {"time": 420, "food": 12, "wood": 6, "gold": 4, "stone": 0},
                    {"time": 600, "food": 12, "wood": 9, "gold": 4, "stone": 0},
                    {"time": 720, "food": 16, "wood": 9, "gold": 4, "stone": 0},
                    {"time": 900, "food": 18, "wood": 9, "gold": 4, "stone": 0},
                    {"time": 1020, "food": 20, "wood": 11, "gold": 8, "stone": 0}
                ],
                "variations": [
                    {
                        "name": "Defensive variation",
                        "description": "Build a castle in your base before making knights",
                        "adjustments": "Send 5 villagers to stone after clicking up to Castle Age"
                    },
                    {
                        "name": "Aggressive variation",
                        "description": "Add a siege workshop and create mangonels for early push",
                        "adjustments": "Transfer some gold villagers to wood for mangonels"
                    }
                ],
                "videos": [
                    {
                        "title": "Fast Castle into Knights by St4rk",
                        "url": "https://www.youtube.com/watch?v=WtukDHXy9Fc",
                        "author": "St4rk"
                    }
                ],
                "tips": [
                    "Use your free farm upgrades to maximize food income",
                    "Take advantage of the Franks cavalry HP bonus in fights",
                    "Use the castle discount to secure important areas on the map",
                    "Consider transitioning to Throwing Axemen against civilizations with strong camel units"
                ],
                "featured": True
            },
            {
                "id": "britons_archers",
                "name": "Britons Archer Rush",
                "description": "Standard archer build with Britons",
                "type": "Rush",
                "difficulty": "Easy",
                "primary_goal": "Apply early feudal pressure with archers",
                "execution_time": 840,  # 14:00 minutes
                "creator": "Hera",
                "meta_relevance": "High",
                "suitable_maps": ["Arabia", "Four Lakes", "Gold Rush"],
                "ideal_civilizations": ["Britons", "Mayans", "Ethiopians"],
                "matchups": {
                    "good_against": ["Franks", "Persians", "Goths"],
                    "bad_against": ["Eagle Warriors", "Skirmishers", "Mangonels"]
                },
                "steps": [
                    {
                        "population": 6,
                        "age": "dark",
                        "time": 0,
                        "instruction": "Send first 6 villagers to sheep"
                    },
                    {
                        "population": 7,
                        "age": "dark",
                        "time": 25,
                        "instruction": "Build house with 7th villager, then to sheep"
                    },
                    {
                        "population": 10,
                        "age": "dark",
                        "time": 120,
                        "instruction": "Build lumber camp with 10th villager, then send 10-13 to wood"
                    },
                    {
                        "population": 14,
                        "age": "dark",
                        "time": 210,
                        "instruction": "Send 14-15 to berries, build mill"
                    },
                    {
                        "population": 16,
                        "age": "dark",
                        "time": 240,
                        "instruction": "Build house with 16th villager, send to berries"
                    },
                    {
                        "population": 17,
                        "age": "dark",
                        "time": 270,
                        "instruction": "Send 17th villager to build a house, then to wood"
                    },
                    {
                        "population": 21,
                        "age": "dark",
                        "time": 350,
                        "instruction": "Send 18-21 to wood"
                    },
                    {
                        "population": 22,
                        "age": "dark",
                        "time": 380,
                        "instruction": "Click up to Feudal Age"
                    },
                    {
                        "population": 23,
                        "age": "dark",
                        "time": 420,
                        "instruction": "Send 22-23 to gold, build mining camp"
                    },
                    {
                        "population": 25,
                        "age": "feudal",
                        "time": 550,
                        "instruction": "Reach Feudal Age. Build 2 archery ranges."
                    },
                    {
                        "population": 27,
                        "age": "feudal",
                        "time": 600,
                        "instruction": "Start producing archers. Send 24-27 to gold."
                    },
                    {
                        "population": 28,
                        "age": "feudal",
                        "time": 630,
                        "instruction": "Research Double-Bit Axe for wood upgrades"
                    },
                    {
                        "population": 30,
                        "age": "feudal",
                        "time": 690,
                        "instruction": "Build blacksmith, research fletching"
                    },
                    {
                        "population": 35,
                        "age": "feudal",
                        "time": 780,
                        "instruction": "Have at least 8-10 archers, attack enemy"
                    },
                    {
                        "population": 40,
                        "age": "feudal",
                        "time": 840,
                        "instruction": "Continue archer production, build a third range"
                    }
                ],
                "villager_assignments": [
                    {"time": 0, "food": 6, "wood": 0, "gold": 0, "stone": 0},
                    {"time": 120, "food": 9, "wood": 3, "gold": 0, "stone": 0},
                    {"time": 210, "food": 9, "wood": 7, "gold": 0, "stone": 0},
                    {"time": 380, "food": 11, "wood": 10, "gold": 0, "stone": 0},
                    {"time": 420, "food": 11, "wood": 10, "gold": 2, "stone": 0},
                    {"time": 550, "food": 11, "wood": 10, "gold": 4, "stone": 0},
                    {"time": 600, "food": 11, "wood": 10, "gold": 8, "stone": 0},
                    {"time": 840, "food": 14, "wood": 12, "gold": 10, "stone": 0}
                ],
                "variations": [
                    {
                        "name": "Fast Castle variation",
                        "description": "Transition to Castle Age for Crossbowmen",
                        "adjustments": "Build market and blacksmith around population 32"
                    },
                    {
                        "name": "Skirmisher defense",
                        "description": "If enemy makes skirmishers, mix in some scouts",
                        "adjustments": "Build a stable and make 4-5 scouts to deal with enemy skirmishers"
                    }
                ],
                "videos": [
                    {
                        "title": "Britons Archer Build Order",
                        "url": "https://www.youtube.com/watch?v=iNBDMjF3L3A",
                        "author": "Hera"
                    }
                ],
                "tips": [
                    "Use your extra range in Castle Age to kite enemy units",
                    "Keep your archers together for maximum effectiveness",
                    "Focus on economy behind your archer pressure",
                    "Take advantage of cheaper Town Centers in Castle Age"
                ],
                "featured": True
            },
            {
                "id": "aztecs_drush_fc",
                "name": "Aztecs Drush Fast Castle",
                "description": "Drush into Fast Castle with Monks and Eagles",
                "type": "Drush FC",
                "difficulty": "Hard",
                "primary_goal": "Apply early pressure with militia, then boom to Castle Age",
                "execution_time": 1080,  # 18:00 minutes
                "creator": "Viper",
                "meta_relevance": "High",
                "suitable_maps": ["Arabia", "Ghost Lake", "Gold Rush"],
                "ideal_civilizations": ["Aztecs", "Mayans", "Incas"],
                "matchups": {
                    "good_against": ["Britons", "Franks", "Turks"],
                    "bad_against": ["Byzantine", "Spanish", "Goths"]
                },
                "steps": [
                    {
                        "population": 6,
                        "age": "dark",
                        "time": 0,
                        "instruction": "Send first 6 villagers to sheep"
                    },
                    {
                        "population": 7,
                        "age": "dark",
                        "time": 25,
                        "instruction": "Build house with 7th villager, then to sheep"
                    },
                    {
                        "population": 10,
                        "age": "dark",
                        "time": 120,
                        "instruction": "Build lumber camp with 10th villager, then send 10-12 to wood"
                    },
                    {
                        "population": 13,
                        "age": "dark",
                        "time": 180,
                        "instruction": "13th villager builds house, then to sheep"
                    },
                    {
                        "population": 14,
                        "age": "dark",
                        "time": 210,
                        "instruction": "Send 14-16 to berries, build mill"
                    },
                    {
                        "population": 17,
                        "age": "dark",
                        "time": 270,
                        "instruction": "Build barracks with 17th villager, then to gold"
                    },
                    {
                        "population": 19,
                        "age": "dark",
                        "time": 330,
                        "instruction": "Build house, mine camp and send 18-20 to gold"
                    },
                    {
                        "population": 20,
                        "age": "dark",
                        "time": 360,
                        "instruction": "Create 3 militia from barracks for drush"
                    },
                    {
                        "population": 23,
                        "age": "dark",
                        "time": 450,
                        "instruction": "Send 21-23 to wood"
                    },
                    {
                        "population": 24,
                        "age": "dark",
                        "time": 480,
                        "instruction": "Attack with your 3 militia, harass enemy economy"
                    },
                    {
                        "population": 27,
                        "age": "dark",
                        "time": 510,
                        "instruction": "Send 24-27 to food (farms), click up to Feudal Age"
                    },
                    {
                        "population": 29,
                        "age": "feudal",
                        "time": 690,
                        "instruction": "Reach Feudal Age. Build market and blacksmith."
                    },
                    {
                        "population": 31,
                        "age": "feudal",
                        "time": 750,
                        "instruction": "Click up to Castle Age"
                    },
                    {
                        "population": 33,
                        "age": "castle",
                        "time": 930,
                        "instruction": "Reach Castle Age. Build monastery, start creating monks"
                    },
                    {
                        "population": 36,
                        "age": "castle",
                        "time": 1000,
                        "instruction": "Build siege workshop, create mangonels for support"
                    },
                    {
                        "population": 40,
                        "age": "castle",
                        "time": 1080,
                        "instruction": "Create Eagle Warriors and push with monks, eagles and siege"
                    }
                ],
                "villager_assignments": [
                    {"time": 0, "food": 6, "wood": 0, "gold": 0, "stone": 0},
                    {"time": 120, "food": 9, "wood": 3, "gold": 0, "stone": 0},
                    {"time": 210, "food": 9, "wood": 6, "gold": 0, "stone": 0},
                    {"time": 330, "food": 12, "wood": 6, "gold": 4, "stone": 0},
                    {"time": 450, "food": 12, "wood": 9, "gold": 4, "stone": 0},
                    {"time": 510, "food": 16, "wood": 9, "gold": 4, "stone": 0},
                    {"time": 750, "food": 18, "wood": 9, "gold": 6, "stone": 0},
                    {"time": 930, "food": 18, "wood": 11, "gold": 8, "stone": 0},
                    {"time": 1080, "food": 18, "wood": 13, "gold": 12, "stone": 0}
                ],
                "variations": [
                    {
                        "name": "Heavy monk play",
                        "description": "Focus more on monks and relics",
                        "adjustments": "Send more villagers to gold and research monastery technologies"
                    },
                    {
                        "name": "Eagle Warrior rush",
                        "description": "Faster Eagle Warrior production",
                        "adjustments": "Build multiple barracks in Castle Age"
                    }
                ],
                "videos": [
                    {
                        "title": "Aztecs Drush FC by Viper",
                        "url": "https://www.youtube.com/watch?v=dMJIzMB4M6s",
                        "author": "Viper"
                    }
                ],
                "tips": [
                    "Use your free loom and faster military production",
                    "Collect as many relics as possible for extra gold",
                    "Use your villager carry bonus to optimize resource collection",
                    "Mix Eagle Warriors with siege and monks for a powerful combination"
                ],
                "featured": True
            }
        ]
    }
    
    # Sample maps data
    maps_data = {
        "maps": [
            {
                "id": "arabia",
                "name": "Arabia",
                "type": "Open",
                "resources": "Standard",
                "characteristics": [
                    "Open map with few forests",
                    "Each player starts with standard resources near their base",
                    "Resources are more exposed and less defensible",
                    "Aggressive early play is common"
                ],
                "top_civilizations": ["Franks", "Mongols", "Huns", "Mayans", "Aztecs"],
                "recommended_strategies": [
                    "Scout/Archer rush in Feudal Age",
                    "Knights/Crossbowmen in Castle Age",
                    "Aggressive play is rewarded"
                ],
                "image_path": "assets/images/maps/arabia.jpg"
            },
            {
                "id": "arena",
                "name": "Arena",
                "type": "Closed",
                "resources": "Standard",
                "characteristics": [
                    "Each player starts inside stone walls",
                    "Safe booming conditions in early game",
                    "Standard resources within walls",
                    "Favors civilizations with strong economy or late-game power"
                ],
                "top_civilizations": ["Aztecs", "Mayans", "Byzantines", "Teutons", "Turks"],
                "recommended_strategies": [
                    "Fast Castle into Unique Units/Knights",
                    "Monk and Siege pushes",
                    "Heavy booming into Imperial Age"
                ],
                "image_path": "assets/images/maps/arena.jpg"
            },
            {
                "id": "islands",
                "name": "Islands",
                "type": "Water",
                "resources": "High",
                "characteristics": [
                    "Players start on separate islands",
                    "Naval control is essential",
                    "More gold and stone than standard maps",
                    "Land attacks require transport ships"
                ],
                "top_civilizations": ["Japanese", "Vikings", "Italians", "Portuguese", "Malay"],
                "recommended_strategies": [
                    "Fast Feudal into Galleys",
                    "Securing fishing ships early",
                    "Controlling water before landing"
                ],
                "image_path": "assets/images/maps/islands.jpg"
            }
        ]
    }
    
    # Save data files if they don't exist
    files_to_create = [
        ('assets/data/civilizations.json', civilizations_data),
        ('assets/data/build_orders.json', build_orders_data),
        ('assets/data/maps.json', maps_data)
    ]
    
    for file_path, data in files_to_create:
        full_path = app_root / file_path
        if not full_path.exists():
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Created sample data file: {file_path}")
    
    print("Sample data created successfully.")

def create_empty_stats_file():
    """Create an empty statistics file if it doesn't exist."""
    app_root = Path(__file__).parent
    stats_file = app_root / 'assets/data/statistics.json'
    
    if not stats_file.exists():
        empty_stats = {
            "civilization_win_rates": [],
            "build_order_success_rates": [],
            "map_pick_rates": [],
            "last_updated": "2023-01-01"
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(empty_stats, f, indent=2)
        
        print("Created empty statistics file.")

def create_empty_user_data():
    """Create an empty user data file if it doesn't exist."""
    app_root = Path(__file__).parent
    user_data_file = app_root / 'assets/data/user_data.json'
    
    if not user_data_file.exists():
        empty_user_data = {
            "favorites": [],
            "history": [],
            "settings": {
                "preferred_difficulty": "Medium",
                "preferred_civilizations": [],
                "preferred_build_types": [],
                "dark_mode": False
            }
        }
        
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(empty_user_data, f, indent=2)
        
        print("Created empty user data file.")

def initialize_app():
    """Initialize the app by creating all necessary structures."""
    create_directory_structure()
    create_sample_data()
    create_empty_stats_file()
    create_empty_user_data()
    print("Application initialized successfully.")

if __name__ == "__main__":
    initialize_app() 