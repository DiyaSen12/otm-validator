# conversion_logic.py

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ("LB", "KG"): 0.453592,
        ("KG", "LB"): 2.20462,
        ("G", "KG"): 0.001,
        ("KG", "G"): 1000,
        ("L", "ML"): 1000,
        ("ML", "L"): 0.001,
        ("GAL", "L"): 3.78541,
        ("L", "GAL"): 0.264172,
        ("INCH", "CM"): 2.54,
        ("CM", "INCH"): 0.393701
        # Add more as needed
    }

    try:
        factor = conversion_factors[(from_unit.upper(), to_unit.upper())]
        return round(value * factor, 4)
    except KeyError:
        return f"Unsupported conversion from {from_unit} to {to_unit}"
