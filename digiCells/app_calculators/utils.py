def compute_seeding_result(data):
    """
    Calculate cell seeding parameters based on cell counts, viability, and seeding requirements.
    
    This function processes cell count and viability data to calculate:
    - Average cell density in the suspension
    - Number of cells needed per well
    - Total cells required (including buffer)
    - Volume of cell suspension needed for seeding
    - Volume of media needed for dilution
    
    Parameters:
    -----------
    data : dict
        A dictionary containing the following keys:
        - count1, count2, count3 (optional): Cell counts from different measurements
        - viability1, viability2, viability3 (optional): Cell viability percentages from different measurements
        - suspension_volume : float - Volume of the original cell suspension (in mL)
        - seeding_density : float - Target cell seeding density (cells/cm²)
        - surface_area : float - Surface area of each well (in cm²)
        - num_wells : int - Number of wells to be seeded
        - buffer : float - Additional buffer percentage for cells (e.g., 10 for 10% extra)
        - media_volume : float - Media volume per well (in mL)
    
    Returns:
    --------
    dict
        A dictionary containing:
        - cell_density : float - Viable cells per mL in the original suspension
        - cells_per_well : float - Number of cells needed per well
        - required_cells_total : float - Total number of cells required (including buffer)
        - volume_to_seed : float - Volume of cell suspension needed (in mL)
        - volume_to_dilute : float - Volume of media to add for dilution (in mL)
        - volume_per_well_ul : float - Media volume per well (in μL)
    
    Notes:
    ------
    - The function averages multiple cell counts and viability measurements if provided
    - Cell density is calculated as: avg_count * (avg_viability/100) / suspension_volume
    - The number of cells per well is: seeding_density * surface_area
    - Buffer percentage is applied to both total cells and final media volume
    """
    # Collect all available cell counts and viabilities (up to 3 measurements)
    counts = [data.get(f"count{i}") for i in range(1, 4) if data.get(f"count{i}")]
    viabilities = [data.get(f"viability{i}") for i in range(1, 4) if data.get(f"viability{i}")]

    # Calculate average cell count and viability across all measurements
    avg_count = sum(counts) / len(counts)
    avg_viab = sum(viabilities) / len(viabilities)
    
    # Calculate cell density (viable cells/mL) in the original suspension
    # Formula: cell count × viability percentage ÷ suspension volume
    cell_density = avg_count * (avg_viab / 100) / data['suspension_volume']

    # Calculate how many cells are needed per individual well
    # Formula: seeding density (cells/cm²) × surface area of well (cm²)
    cells_per_well = data['seeding_density'] * data['surface_area']
    
    # Calculate total cells needed for all wells
    total_cells = cells_per_well * data['num_wells']
    
    # Add buffer percentage to account for pipetting errors, cell loss, etc.
    total_cells *= (1 + data['buffer'] / 100)

    # Calculate volume of cell suspension needed based on cell density
    # Formula: total cells needed ÷ cell density (cells/mL)
    volume_to_seed = total_cells / cell_density
    
    # Calculate total media volume needed for all wells
    total_media = data['media_volume'] * data['num_wells']
    
    # Add buffer percentage to final volume for safety margin
    final_volume = total_media * (1 + data['buffer'] / 100)
    
    # Calculate additional media needed for dilution
    # Formula: final total volume - volume of cell suspension
    volume_to_dilute = final_volume - volume_to_seed

    # Return all calculated values as a dictionary
    return {
        "cell_density": cell_density,            # Viable cells/mL in original suspension
        "cells_per_well": cells_per_well,        # Number of cells needed in each well
        "required_cells_total": total_cells,     # Total cells needed (with buffer)
        "volume_to_seed": volume_to_seed,        # Volume of cell suspension in mL
        "volume_to_dilute": volume_to_dilute,    # Additional media volume needed in mL
        "volume_per_well_ul": data['media_volume'] * 1000,  # Convert mL to µL per well
    }


