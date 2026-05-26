from ai_orchestra.shared.config import AppConfig, load_setup_config


def test_load_setup_config_defaults() -> None:
    cfg = load_setup_config()
    assert isinstance(cfg, AppConfig)
    assert cfg.app_name == "AI Orchestra 2"

