from src.utils import safe_json_load

def test_safe_json_load():
    assert safe_json_load('{"a":1}') == {"a": 1}
    assert safe_json_load("invalid") is None