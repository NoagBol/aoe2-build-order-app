from .data_loader import load_build_orders, load_civilizations, load_maps

def get_recommended_build_orders(civilization_id=None, build_types=None, map_type=None, 
                                difficulty=None, ally_civs=None, enemy_civs=None):
    """
    Get recommended build orders based on various filters.
    
    Args:
        civilization_id (int): ID of the selected civilization
        build_types (list): List of build order types to filter
        map_type (str): Map type to filter
        difficulty (str): Difficulty level to filter
        ally_civs (list): List of allied civilization names
        enemy_civs (list): List of enemy civilization names
        
    Returns:
        list: List of recommended build orders
    """
    # Load all build orders
    all_build_orders = load_build_orders()
    
    # No filters, return all build orders
    if not civilization_id and not build_types and not map_type and not difficulty and not ally_civs and not enemy_civs:
        return all_build_orders
    
    # Apply filters
    recommended = all_build_orders.copy()
    
    # Filter by civilization compatibility
    if civilization_id:
        # Keep build orders where the civilization is ideal or compatible
        recommended = [bo for bo in recommended if 
                     civilization_id in bo.get("ideal_civilizations", []) or 
                     civilization_id in bo.get("compatible_civilizations", [])]
        
        # Sort by civilization compatibility (ideal > compatible)
        recommended.sort(key=lambda bo: 
                      (civilization_id in bo.get("ideal_civilizations", []), 
                       bo.get("meta_relevance", 0)), 
                      reverse=True)
    
    # Filter by build order type
    if build_types and len(build_types) > 0:
        recommended = [bo for bo in recommended if bo.get("type", "") in build_types]
    
    # Filter by map type
    if map_type:
        recommended = [bo for bo in recommended if map_type in bo.get("suitable_maps", [])]
    
    # Filter by difficulty
    if difficulty:
        recommended = [bo for bo in recommended if bo.get("difficulty", "") == difficulty]
    
    # Consider enemy civilizations
    if enemy_civs and len(enemy_civs) > 0:
        # Load civilization data to get specialties
        all_civs = load_civilizations()
        enemy_civ_specialties = []
        
        # Get the specialties of enemy civilizations
        for enemy_civ_name in enemy_civs:
            for civ in all_civs:
                if civ["name"] == enemy_civ_name:
                    enemy_civ_specialties.extend(civ.get("specialty", []))
        
        # Prioritize build orders that are strong against these specialties
        if enemy_civ_specialties:
            # This is a simplified approach - in a real app, this would be more sophisticated
            for bo in recommended:
                bo["counter_score"] = 0
                for archetype in bo.get("strong_against", []):
                    # Check if the build order is strong against any of the enemy specialties
                    if any(specialty in archetype.lower() for specialty in [s.lower() for s in enemy_civ_specialties]):
                        bo["counter_score"] += 1
            
            # Sort by counter score and meta relevance
            recommended.sort(key=lambda bo: (bo.get("counter_score", 0), bo.get("meta_relevance", 0)), reverse=True)
    
    # No build orders found with the given filters
    if not recommended:
        return []
    
    return recommended

def get_map_civilization_tier_list(map_id):
    """
    Get a tier list of civilizations for a specific map.
    
    Args:
        map_id (int): ID of the map
        
    Returns:
        list: List of civilizations with their tier ranking for this map
    """
    # Load map data
    maps = load_maps()
    selected_map = None
    
    for m in maps:
        if m["id"] == map_id:
            selected_map = m
            break
    
    if not selected_map:
        return []
    
    # Load civilization data
    all_civs = load_civilizations()
    
    # Create a tier list
    tier_list = []
    
    # Get the IDs of strong and weak civilizations for this map
    strong_civ_ids = selected_map.get("strong_civilizations", [])
    weak_civ_ids = selected_map.get("weak_civilizations", [])
    
    # In a real app, this would be based on win rate data for the map
    # Here we'll simulate tiers based on the strong/weak lists
    for civ in all_civs:
        civ_id = civ["id"]
        
        # Determine tier based on whether the civ is in strong/weak lists
        if civ_id in strong_civ_ids[:2]:  # Top 2 in strong list
            tier = "S"
            win_rate = 56.0 + (strong_civ_ids.index(civ_id) * -0.5)  # Simulated win rate
        elif civ_id in strong_civ_ids:  # Rest of strong list
            tier = "A"
            win_rate = 53.0 + (strong_civ_ids.index(civ_id) * -0.3)  # Simulated win rate
        elif civ_id not in weak_civ_ids:  # Not in weak list
            tier = "B"
            win_rate = 50.0 + ((civ_id % 3) - 1)  # Simulated win rate with some variation
        elif civ_id in weak_civ_ids[-2:]:  # Bottom 2 in weak list
            tier = "D"
            win_rate = 46.0 - (weak_civ_ids[::-1].index(civ_id) * 0.5)  # Simulated win rate
        else:  # Rest of weak list
            tier = "C"
            win_rate = 48.0 - (weak_civ_ids.index(civ_id) * 0.3)  # Simulated win rate
        
        # Add to tier list
        tier_list.append({
            "id": civ_id,
            "name": civ["name"],
            "tier": tier,
            "win_rate": round(win_rate, 1),
            "strengths_on_map": _get_civ_map_strengths(civ, selected_map)
        })
    
    # Sort by tier (S, A, B, C, D) and then by win rate
    tier_order = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4}
    tier_list.sort(key=lambda x: (tier_order[x["tier"]], -x["win_rate"]))
    
    return tier_list

def _get_civ_map_strengths(civ, map_data):
    """
    Generate a description of a civilization's strengths on a specific map.
    
    Args:
        civ (dict): Civilization data
        map_data (dict): Map data
        
    Returns:
        str: Description of strengths
    """
    # In a real app, this would be data-driven and more sophisticated
    # Here we'll generate some text based on civ specialty and map type
    
    map_type = map_data.get("type", "")
    specialties = civ.get("specialty", [])
    
    strengths = []
    
    if "Cavalry" in specialties and map_type == "Open":
        strengths.append("Strong mobility on open terrain")
    
    if "Archers" in specialties and map_type == "Open":
        strengths.append("Good map control with ranged units")
    
    if "Infantry" in specialties and map_type == "Closed":
        strengths.append("Strong in chokepoint battles")
    
    if "Economy" in specialties:
        if map_type == "Closed":
            strengths.append("Safe booming potential")
        else:
            strengths.append("Good resource efficiency")
    
    if "Monks" in specialties and map_type == "Closed":
        strengths.append("Excellent relic control")
    
    if "Siege" in specialties and map_type == "Closed":
        strengths.append("Strong in breaking defensive positions")
    
    if "Naval" in specialties and map_type == "Water":
        strengths.append("Dominant water control")
    
    if "Gunpowder" in specialties and map_type == "Closed":
        strengths.append("Powerful late-game options")
    
    # If no specific strengths were found, add a generic one
    if not strengths:
        if civ["id"] in map_data.get("strong_civilizations", []):
            strengths.append("Well-suited for this map type")
        elif civ["id"] in map_data.get("weak_civilizations", []):
            strengths.append("Struggles on this map type")
        else:
            strengths.append("Average performance on this map")
    
    return " | ".join(strengths) 