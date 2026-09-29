from sqlalchemy import select
from sqlalchemy.orm import Session

from services.security_service.app.models.security_model import Security


class SecurityRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_symbol(self, symbol: str) -> Security | None:
        statement = select(Security).where(
            Security.symbol == symbol
        )

        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self) -> list[Security]:
        statement = select(Security).order_by(
            Security.symbol
        )

        return list(
            self.db.execute(statement).scalars().all()
        )

    def create(self, security: Security) -> Security:
        existing_security = self.get_by_symbol(
            security.symbol
        )

        if existing_security is not None:
            raise ValueError(
                f"Security with symbol '{security.symbol}' "
                "already exists."
            )

        self.db.add(security)
        self.db.commit()
        self.db.refresh(security)

        return security

    def update(self, security: Security) -> Security:
        existing_security = self.db.get(
            Security,
            security.id,
        )

        if existing_security is None:
            raise ValueError(
                f"Security with id '{security.id}' "
                "does not exist."
            )

        duplicate_security = self.get_by_symbol(
            security.symbol
        )

        if (
            duplicate_security is not None
            and duplicate_security.id != security.id
        ):
            raise ValueError(
                f"Security with symbol '{security.symbol}' "
                "already belongs to another security."
            )

        self.db.commit()
        self.db.refresh(security)

        return security

    def delete(self, security: Security) -> None:
        existing_security = self.db.get(
            Security,
            security.id,
        )

        if existing_security is None:
            raise ValueError(
                f"Security with id '{security.id}' "
                "does not exist."
            )

        self.db.delete(existing_security)
        self.db.commit()