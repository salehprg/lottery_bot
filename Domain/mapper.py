def map_to_dto(model_instance, dto_class):
    # Get the attributes of the model instance
    model_attributes = model_instance.__dict__
    
    result = {}
    for key in model_attributes:
        if not key.startswith('_'):
            result[key] = model_attributes[key]


    return dto_class(**result)