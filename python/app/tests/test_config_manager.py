from app.config_manager import ConfigManager

def test_cm_is_singleton():
    cm_instance_1 = ConfigManager()
    cm_instance_2 = ConfigManager()
    assert cm_instance_1 is cm_instance_2