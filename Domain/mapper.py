def map_to_dto(model_instance, dto_class):
    # Get the attributes of the model instance
    model_attributes = model_instance.__dict__
    
    # Filter out SQLAlchemy internal attributes (like '_sa_instance_state')
    model_attributes = {k: v for k, v in model_attributes.items() if not k.startswith('_')}
    
    # Create an instance of the DTO class using the filtered attributes
    return dto_class(**model_attributes)