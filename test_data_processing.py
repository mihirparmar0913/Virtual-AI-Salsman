from src.data_processing.feature_normalizer import (
    normalize_feature_name,
    normalize_feature_value,
    parse_ram_gb,
    parse_speed_ghz,
    parse_screen_size_inches,
    parse_storage_gb,
    parse_weight_g    
)

def test_normalize_feature_name():
    assert normalize_feature_name(
        "RAM Memory Installed Size"
    ) == "ram_gb"

    assert normalize_feature_name(
        "CPU Model"
    ) == "processor"

    assert normalize_feature_name(
        "CPU Speed"
    ) == "processor_speed_ghz"

    assert normalize_feature_name(
        "Closure Type"
    ) == "closure_type"


def test_unknown_feature_name():
    assert normalize_feature_name(
        "Some Unknown Feature"
    ) is None


def test_parse_ram_gb():
    assert parse_ram_gb("16 GB") == 16.0
    assert parse_ram_gb("8 GB") == 8.0


def test_parse_ram_mb():
    result = parse_ram_gb("4 MB")

    assert round(result, 4) == round(4 / 1024, 4)


def test_parse_speed_ghz():
    assert parse_speed_ghz("2.4 GHz") == 2.4
    assert parse_speed_ghz("3.2GHz") == 3.2


def test_normalize_feature_value():
    assert normalize_feature_value(
        "ram_gb",
        "16 GB",
    ) == 16.0

    assert normalize_feature_value(
        "processor_speed_ghz",
        "2.4 GHz",
    ) == 2.4

    assert normalize_feature_value(
        "processor",
        "Intel Core i7",
    ) == "Intel Core i7"

def test_parse_screen_size_inches():
    result = parse_screen_size_inches(
        "39.6 Centimetres"
    )

    assert round(result, 2) == 15.59


def test_parse_screen_size_inches_already_inches():
    result = parse_screen_size_inches(
        "15.6 inches"
    )

    assert result == 15.6
def test_parse_storage_gb():
    result = parse_storage_gb("512 GB")
    assert result == 512.0


def test_parse_storage_tb():
    result = parse_storage_gb("1 TB")
    assert result == 1024.0

def test_parse_weight_grams():
    result = parse_weight_g("65 g")
    assert result == 65.0


def test_parse_weight_kilograms():
    result = parse_weight_g("0.8 Kilograms")
    assert result == 800.0


def test_parse_weight_pounds():
    result = parse_weight_g("0.43 Pounds")
    assert round(result, 2) == 195.04
