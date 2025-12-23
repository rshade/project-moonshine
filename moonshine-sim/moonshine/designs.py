class Dimensions:
    """
    Physical Constraints for the Hardware Tracks.
    """
    
    RICKHOUSE_2U = {
        "name": "The Rickhouse",
        "max_height_mm": 88,
        "rack_depth_mm": 700,
        "condenser_type": "Horizontal Axial",
        "pump_required": True
    }
    
    TOWER_V1 = {
        "name": "The Moonshine Tower",
        "max_footprint_mm": [140, 140],
        "max_height_mm": 400,
        "condenser_type": "Vertical Gravity-Fed",
        "pump_required": True # Mandated to prevent zeotropic fractionation
    }