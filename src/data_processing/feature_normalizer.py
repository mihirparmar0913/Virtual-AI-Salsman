import re


# --------------------------------------------------
# Raw feature name -> canonical feature name
# --------------------------------------------------

FEATURE_NAME_MAP = {
    # General
    "Brand": "brand",
    "Colour": "colour",
    "Color": "colour",

    # Computer / smartphone
    "RAM Memory Installed Size": "ram_gb",
    "RAM Memory Installed": "ram_gb",
    "CPU Model": "processor",
    "Processor": "processor",
    "PROCESSOR": "processor",
    "CPU Speed": "processor_speed_ghz",
    "Operating System": "operating_system",
    "Screen Size": "screen_size_inches",
    "Hard Disk Size": "storage",
    
    # Audio
    "Connectivity Technology": "connectivity",
    "Audio Output Mode": "audio_output_mode",
    "Ear Placement": "ear_placement",
    "Special Feature": "special_features",

    # Speakers
    "Speaker Maximum Output Power": "speaker_output_power_w",

    # Watches
    "Watch movement type": "watch_movement",
    "Watch Movement Type": "watch_movement",
    "Band material type": "band_material",
    "Band Material Type": "band_material",
    "Band colour": "band_colour",
    "Case diameter": "case_diameter",
    "Case Diameter": "case_diameter",
    "Water resistance level": "water_resistance",

    # Footwear
    "Material": "material",
    "Material type": "material",
    "Material Type": "material",
    "Sole material": "sole_material",
    "Sole Material": "sole_material",
    "Heel type": "heel_type",
    "Closure type": "closure_type",
    "Closure Type": "closure_type",

    # Clothing
    "Fit type": "fit",
    "Fit Type": "fit",
    "Style": "style",

   
}


def normalize_feature_name(feature_name):
    """
    Convert a raw feature name into a canonical feature name.

    Returns None when the feature is not currently supported.
    """
    if not isinstance(feature_name, str):
        return None

    feature_name = feature_name.strip()

    return FEATURE_NAME_MAP.get(feature_name)


# --------------------------------------------------
# Value normalization helpers
# --------------------------------------------------

def parse_ram_gb(value):
    """
    Convert a RAM value into GB.

    Examples:
        "16 GB" -> 16.0
        "4 GB"  -> 4.0
        "4 MB"  -> 0.0039
    """
    if not isinstance(value, str):
        return None

    match = re.search(
        r"([\d.]+)\s*(GB|MB)",
        value.upper(),
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2)

    if unit == "GB":
        return number

    if unit == "MB":
        return number / 1024

    return None


def parse_speed_ghz(value):
    """
    Convert CPU speed into GHz.

    Examples:
        "2.4 GHz" -> 2.4
        "3.2GHz"  -> 3.2
    """
    if not isinstance(value, str):
        return None

    match = re.search(
        r"([\d.]+)\s*GHz",
        value,
        re.IGNORECASE,
    )

    if not match:
        return None

    return float(match.group(1))
def parse_screen_size_inches(value):
    """
    Convert screen size to inches.

    Examples:
        "39.6 Centimetres" -> approximately 15.59
        "15.6 inches" -> 15.6
    """
    if not isinstance(value, str):
        return None

    match = re.search(
        r"([\d.]+)\s*(Centimetres|Centimeters|cm|inches|inch)",
        value,
        re.IGNORECASE,
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2).lower()

    if unit in {"centimetres", "centimeters", "cm"}:
        return number / 2.54

    return number

def normalize_feature_value(canonical_name, value):
    """
    Normalize a feature value according to its canonical name.
    """
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    if canonical_name == "ram_gb":
        return parse_ram_gb(value)

    if canonical_name == "processor_speed_ghz":
        return parse_speed_ghz(value)

    if canonical_name == "screen_size_inches":
        return parse_screen_size_inches(value)

    return value