from app.config_manager import ConfigManager

def test_cm_is_singleton():
    cm_instance_1 = ConfigManager()
    cm_instance_2 = ConfigManager()
    assert cm_instance_1 is cm_instance_2

def test_cm_has_user_property():
    assert hasattr(ConfigManager(), "user")

def test_cm_hash_connection_manager_property():
    assert hasattr(ConfigManager(), "connection_manager")

def test_cm_hash_contract_property():
    assert hasattr(ConfigManager(), "contrato")