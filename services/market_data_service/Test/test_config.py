from App.config import settings


def test_app_name():
    assert settings.app_name == "InvestIQ"


def test_app_environment():
    assert settings.app_env == "development"