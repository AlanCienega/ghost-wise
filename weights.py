

def calculate_entity_weights(entities):
    num_entities = len(entities)
    max_weight = 5
    min_weight = 1
    weights = {}
    
    if num_entities == 0:
        return weights
    
    # Calcular el rango de pesos
    weight_range = max_weight - min_weight + 1
    
    # Calcular el paso entre cada nivel de peso
    step = num_entities // weight_range
    
    # Asignar pesos a las entidades
    current_weight = max_weight
    current_step = 1
    for entity in entities:
        weights[entity] = current_weight
        current_step += 1
        if current_step > step:
            current_weight -= 1
            current_step = 1
            
    return weights