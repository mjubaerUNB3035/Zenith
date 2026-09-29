from services.security_service.app.database.database import SessionLocal
from services.security_service.app.models.security_model import Security
from services.security_service.app.repositories.security_repository import SecurityRepository


def test_security_repository_crud():
    db = SessionLocal()
    repository = SecurityRepository(db)

    try:
        security = Security(
            symbol="ZENITH_TEST",
            company_name="Zenith Test Company",
            exchange="TEST",
            sector="Technology",
            industry="Software",
            country="Canada",
            active=True,
        )

        # Create
        created = repository.create(security)

        assert created.id is not None

        # Read one
        found = repository.get_by_symbol("ZENITH_TEST")

        assert found is not None
        assert found.company_name == "Zenith Test Company"

        # Read all
        securities = repository.get_all()

        assert any(
            item.symbol == "ZENITH_TEST"
            for item in securities
        )

        # Update
        found.company_name = "Zenith Updated Company"

        updated = repository.update(found)

        assert updated.company_name == "Zenith Updated Company"

        # Delete
        repository.delete(found)

        assert repository.get_by_symbol("ZENITH_TEST") is None

    finally:
        existing = repository.get_by_symbol("ZENITH_TEST")

        if existing is not None:
            repository.delete(existing)

        db.close()