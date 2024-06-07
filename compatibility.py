def calculate_compatibility_entities(profile_entities, cv_entities):
    profile_entities_lower = [entity.lower() for entity in profile_entities]
    cv_entities_lower = [entity.lower() for entity in cv_entities]
    
    profile_entities_set = set(profile_entities_lower)
    cv_entities_set = set(cv_entities_lower)
    
    common_entities = profile_entities_set.intersection(cv_entities_set)
    
    total_entities = len(profile_entities_set)
    if total_entities == 0:
        return 0
    
    compatibility_score = len(common_entities) / total_entities * 100
    return compatibility_score
