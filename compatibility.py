def calculate_compatibility_entities(profile_entities, cv_entities, weights):
    profile_entities_lower = [entity.lower() for entity in profile_entities]
    cv_entities_lower = [entity.lower() for entity in cv_entities]
    
    profile_entities_set = set(profile_entities_lower)
    cv_entities_set = set(cv_entities_lower)
    
    common_entities = profile_entities_set.intersection(cv_entities_set)
    
    total_weight = 0
    common_weight = 0
    
    # Calculate total weight of profile entities
    for entity in profile_entities_set:
        total_weight += weights.get(entity, 0)
    
    # Calculate common weight
    for entity in common_entities:
        common_weight += weights.get(entity, 0)
    
    # Calculate compatibility score
    if total_weight == 0:
        return 0
    
    compatibility_score = (common_weight / total_weight) * 100
    return compatibility_score
