def calculate_compatibility_entities(profile_entities, cv_entities):
    common_entities = set(profile_entities).intersection(set(cv_entities))
    
    total_entities = len(profile_entities)
    if total_entities == 0:
        return 0
    
    compatibility_score = len(common_entities) / total_entities * 100
    return compatibility_score
