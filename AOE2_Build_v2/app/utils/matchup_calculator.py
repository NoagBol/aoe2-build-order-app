from .data_loader import load_civilizations, load_matchup_data

def calculate_team_matchup(your_team, enemy_team):
    """
    Calculate the matchup analysis between two teams.
    
    Args:
        your_team (list): List of civilization dictionaries for your team
        enemy_team (list): List of civilization dictionaries for enemy team
        
    Returns:
        dict: Analysis of the team matchup
    """
    # Calculate team synergy scores
    your_team_synergy = calculate_team_synergy(your_team)
    enemy_team_synergy = calculate_team_synergy(enemy_team)
    
    # Calculate team matchup matrix
    matchup_matrix = []
    overall_win_rate = 0
    
    for your_civ in your_team:
        row = []
        for enemy_civ in enemy_team:
            matchup_data = load_matchup_data(your_civ["id"], enemy_civ["id"])
            row.append(matchup_data.get("win_rate", 50))
            overall_win_rate += matchup_data.get("win_rate", 50)
        matchup_matrix.append(row)
    
    # Calculate average win rate across all matchups
    total_matchups = len(your_team) * len(enemy_team)
    average_win_rate = overall_win_rate / total_matchups if total_matchups > 0 else 50
    
    # Determine advantage level
    if average_win_rate >= 55:
        advantage_level = "Strong Advantage"
    elif average_win_rate >= 52.5:
        advantage_level = "Moderate Advantage"
    elif average_win_rate >= 50.5:
        advantage_level = "Slight Advantage"
    elif average_win_rate >= 49.5:
        advantage_level = "Even"
    elif average_win_rate >= 47.5:
        advantage_level = "Slight Disadvantage"
    elif average_win_rate >= 45:
        advantage_level = "Moderate Disadvantage"
    else:
        advantage_level = "Strong Disadvantage"
    
    # Get team strengths
    your_team_strengths = get_team_strengths(your_team)
    enemy_team_strengths = get_team_strengths(enemy_team)
    
    # Generate recommended strategies
    recommended_strategies = generate_team_strategies(your_team, enemy_team, average_win_rate)
    
    # Create overall assessment
    if average_win_rate >= 52.5:
        overall_assessment = "Your team has an advantage in this matchup. "
    elif average_win_rate <= 47.5:
        overall_assessment = "The enemy team has an advantage in this matchup. "
    else:
        overall_assessment = "This is a relatively even matchup. "
    
    if your_team_synergy > enemy_team_synergy + 1:
        overall_assessment += "Your team composition has better synergy than the enemy's."
    elif enemy_team_synergy > your_team_synergy + 1:
        overall_assessment += "The enemy team composition has better synergy than yours."
    else:
        overall_assessment += "Both teams have similar levels of synergy."
    
    return {
        "your_team_synergy": your_team_synergy,
        "enemy_team_synergy": enemy_team_synergy,
        "matchup_matrix": matchup_matrix,
        "average_win_rate": average_win_rate,
        "advantage_level": advantage_level,
        "your_team_strengths": your_team_strengths,
        "enemy_team_strengths": enemy_team_strengths,
        "recommended_strategies": recommended_strategies,
        "overall_assessment": overall_assessment
    }

def calculate_team_synergy(team):
    """
    Calculate the synergy score for a team composition.
    
    Args:
        team (list): List of civilization dictionaries
        
    Returns:
        float: Synergy score (0-10)
    """
    if not team:
        return 0
    
    # Base synergy score
    synergy = 5.0
    
    # In a real app, this would be based on data and more sophisticated logic
    # Here we'll use a simplified approach
    
    # Check for specialty diversity
    specialties = []
    for civ in team:
        specialties.extend(civ.get("specialty", []))
    
    unique_specialties = set(specialties)
    
    # Bonus for having diverse specialties
    if len(unique_specialties) >= 4:
        synergy += 1.5
    elif len(unique_specialties) >= 3:
        synergy += 1.0
    elif len(unique_specialties) >= 2:
        synergy += 0.5
    
    # Check for key specialties
    if "Cavalry" in unique_specialties:
        synergy += 0.5
    if "Archers" in unique_specialties:
        synergy += 0.5
    if "Economy" in unique_specialties:
        synergy += 0.5
    
    # Check for complementary specialties
    if "Cavalry" in unique_specialties and "Archers" in unique_specialties:
        synergy += 0.5  # Good combination for standard play
    if "Siege" in unique_specialties and "Infantry" in unique_specialties:
        synergy += 0.5  # Good for pushing
    if "Economy" in unique_specialties and "Monks" in unique_specialties:
        synergy += 0.3  # Good for booming and controlling relics
    
    # Check for too much overlap (penalties)
    specialty_counts = {}
    for spec in specialties:
        specialty_counts[spec] = specialty_counts.get(spec, 0) + 1
    
    # Penalty for too much overlap in primary specialties
    for spec, count in specialty_counts.items():
        if count > 2 and spec in ["Cavalry", "Archers", "Infantry"]:
            synergy -= 0.3 * (count - 2)  # Penalty for having too many of the same primary specialty
    
    # Check team bonuses (in a real app, this would analyze actual bonuses)
    # Here we'll simulate it based on team size
    if len(team) >= 3:
        synergy += 0.5  # Bonus for having more team bonuses
    
    # Ensure synergy score is between 1 and 10
    return max(1, min(10, synergy))

def get_team_strengths(team):
    """
    Get the strengths of a team composition.
    
    Args:
        team (list): List of civilization dictionaries
        
    Returns:
        list: List of team strengths
    """
    if not team:
        return []
    
    # In a real app, this would be based on data and more sophisticated logic
    # Here we'll use a simplified approach
    
    strengths = []
    specialties = []
    
    for civ in team:
        specialties.extend(civ.get("specialty", []))
    
    specialty_counts = {}
    for spec in specialties:
        specialty_counts[spec] = specialty_counts.get(spec, 0) + 1
    
    # Add strengths based on specialty counts
    if specialty_counts.get("Cavalry", 0) >= 2:
        strengths.append("Strong cavalry presence")
    
    if specialty_counts.get("Archers", 0) >= 2:
        strengths.append("Powerful ranged firepower")
    
    if specialty_counts.get("Infantry", 0) >= 2:
        strengths.append("Solid frontline infantry")
    
    if specialty_counts.get("Economy", 0) >= 1:
        strengths.append("Good economic potential")
    
    if specialty_counts.get("Monks", 0) >= 1:
        strengths.append("Effective relic control")
    
    if specialty_counts.get("Naval", 0) >= 1:
        strengths.append("Strong water presence")
    
    if specialty_counts.get("Siege", 0) >= 1:
        strengths.append("Powerful siege capabilities")
    
    # Check for diverse strengths
    if len(specialty_counts) >= 4:
        strengths.append("Well-rounded team composition")
    
    # Check for specific civilization strengths (in a real app, this would be more specific)
    for civ in team:
        if civ.get("name") == "Franks":
            strengths.append("Strong Knight rush potential")
        elif civ.get("name") == "Britons":
            strengths.append("Excellent archer range advantage")
        elif civ.get("name") == "Aztecs":
            strengths.append("Powerful monks and economy")
    
    return strengths

def generate_team_strategies(your_team, enemy_team, win_rate):
    """
    Generate recommended team strategies based on team compositions.
    
    Args:
        your_team (list): List of civilization dictionaries for your team
        enemy_team (list): List of civilization dictionaries for enemy team
        win_rate (float): Your team's average win rate against the enemy team
        
    Returns:
        list: List of recommended strategies
    """
    strategies = []
    
    # In a real app, this would be based on data and more sophisticated logic
    # Here we'll use a simplified approach
    
    # Get team specialties
    your_specialties = []
    enemy_specialties = []
    
    for civ in your_team:
        your_specialties.extend(civ.get("specialty", []))
    
    for civ in enemy_team:
        enemy_specialties.extend(civ.get("specialty", []))
    
    # Count specialties
    your_specialty_counts = {}
    for spec in your_specialties:
        your_specialty_counts[spec] = your_specialty_counts.get(spec, 0) + 1
    
    enemy_specialty_counts = {}
    for spec in enemy_specialties:
        enemy_specialty_counts[spec] = enemy_specialty_counts.get(spec, 0) + 1
    
    # Generate strategies based on your team's strengths
    if your_specialty_counts.get("Cavalry", 0) >= 2:
        if "Infantry" in enemy_specialty_counts:
            strategies.append("Use your cavalry advantage to raid and avoid direct engagements with enemy infantry")
        else:
            strategies.append("Coordinate knight rushes from multiple players")
    
    if your_specialty_counts.get("Archers", 0) >= 2:
        if "Cavalry" in enemy_specialty_counts:
            strategies.append("Mass archers together and protect with spearmen against enemy cavalry")
        else:
            strategies.append("Focus on massing archers and applying pressure")
    
    if your_specialty_counts.get("Economy", 0) >= 2:
        strategies.append("Prioritize booming and supporting teammates with resources")
    
    # Generate strategies based on enemy team's composition
    if enemy_specialty_counts.get("Cavalry", 0) >= 2:
        strategies.append("Prepare defenses against cavalry raids, especially pikemen")
    
    if enemy_specialty_counts.get("Archers", 0) >= 2:
        strategies.append("Consider making skirmishers or siege to counter enemy archers")
    
    if enemy_specialty_counts.get("Economy", 0) >= 2:
        strategies.append("Apply early pressure to disrupt enemy economy")
    
    # General strategies based on win rate
    if win_rate >= 55:
        strategies.append("Press your advantage with aggressive play")
    elif win_rate <= 45:
        strategies.append("Play defensively and focus on team coordination")
    else:
        strategies.append("Focus on map control and adapting to the enemy's strategy")
    
    # Ensure we have at least 3 strategies
    if len(strategies) < 3:
        default_strategies = [
            "Coordinate timing attacks with your team",
            "Control key map resources as a team",
            "Share resources between players based on civilization needs"
        ]
        
        for strategy in default_strategies:
            if strategy not in strategies:
                strategies.append(strategy)
                if len(strategies) >= 3:
                    break
    
    return strategies

def get_counter_strategies(enemy_civs):
    """
    Get recommended counter civilizations against a set of enemy civilizations.
    
    Args:
        enemy_civs (list): List of enemy civilization dictionaries
        
    Returns:
        list: List of recommended counter civilizations
    """
    # Load all civilizations
    all_civs = load_civilizations()
    
    # In a real app, this would be based on matchup data
    # Here we'll use a simplified approach
    
    # Get enemy specialties
    enemy_specialties = []
    for civ in enemy_civs:
        enemy_specialties.extend(civ.get("specialty", []))
    
    # Count specialties
    specialty_counts = {}
    for spec in enemy_specialties:
        specialty_counts[spec] = specialty_counts.get(spec, 0) + 1
    
    # Calculate counter scores for each civilization
    counter_civs = []
    
    for civ in all_civs:
        # Skip if the civilization is in the enemy team
        if any(e["id"] == civ["id"] for e in enemy_civs):
            continue
        
        counter_score = 5  # Base score
        counter_reason = ""
        
        # Check for counters to enemy specialties
        if specialty_counts.get("Cavalry", 0) >= 2 and "Infantry" in civ.get("specialty", []):
            counter_score += 2
            counter_reason = "Strong infantry counters enemy cavalry focus"
        elif specialty_counts.get("Archers", 0) >= 2 and "Cavalry" in civ.get("specialty", []):
            counter_score += 2
            counter_reason = "Cavalry can close distance against enemy archers"
        elif specialty_counts.get("Infantry", 0) >= 2 and "Archers" in civ.get("specialty", []):
            counter_score += 2
            counter_reason = "Archers effective against enemy infantry focus"
        elif "Economy" in civ.get("specialty", []) and not any(spec in ["Economy", "Monks"] for spec in enemy_specialties):
            counter_score += 1
            counter_reason = "Economic advantage against aggressive enemies"
        else:
            # Look at specific civilizations (in a real app, this would use real matchup data)
            for enemy_civ in enemy_civs:
                if enemy_civ["name"] == "Franks" and "Infantry" in civ.get("specialty", []):
                    counter_score += 1
                    counter_reason = "Infantry counters Frankish cavalry"
                elif enemy_civ["name"] == "Britons" and "Cavalry" in civ.get("specialty", []):
                    counter_score += 1
                    counter_reason = "Cavalry can close distance on Britons' archers"
                elif enemy_civ["name"] == "Aztecs" and "Cavalry" in civ.get("specialty", []):
                    counter_score += 1
                    counter_reason = "Cavalry effective against Aztecs' lack of cavalry"
        
        # If no specific counter was found, provide a general reason
        if not counter_reason:
            specialty_str = ", ".join(civ.get("specialty", [])[:2])
            counter_reason = f"Balanced choice with {specialty_str} strengths"
        
        # Add to list
        counter_civs.append({
            "id": civ["id"],
            "name": civ["name"],
            "counter_score": min(10, counter_score),
            "counter_reason": counter_reason,
            "icon_path": civ.get("icon_path")
        })
    
    # Sort by counter score
    counter_civs.sort(key=lambda x: x["counter_score"], reverse=True)
    
    # Return top 6 counters
    return counter_civs[:6] 