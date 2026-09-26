from services.market_data_service.app.config import settings


def test_app_name():
    assert settings.app_name == "Zenith"


def test_app_environment():
    assert settings.app_env == "development"