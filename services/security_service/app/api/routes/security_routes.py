from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.security_service.app.database.database import SessionLocal
from services.security_service.app.models.security_model import Security
from services.security_service.app.repositories.security_repository import (
    SecurityRepository,
)
from services.security_service.app.ingestion.security_ingestor import (
    SecurityIngestor,
)
from services.security_service.app.api.schemas.security_schema import (
    SecurityCreate,
    SecurityUpdate,
    SecurityResponse,
)


router = APIRouter(
    prefix="/securities",
    tags=["Security"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{symbol}",
    response_model=SecurityResponse,
)
def fetch_security(
    symbol: str,
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)

    security = repository.get_by_symbol(
        symbol.upper()
    )

    if security is None:
        raise HTTPException(
            status_code=404,
            detail=f"Security '{symbol.upper()}' not found.",
        )

    return security


@router.get(
    "/",
    response_model=list[SecurityResponse],
)
def fetch_all_securities(
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)

    return repository.get_all()


@router.post(
    "/",
    response_model=SecurityResponse,
    status_code=201,
)
def create_security(
    security_data: SecurityCreate,
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)

    security = Security(
        symbol=security_data.symbol.upper(),
        company_name=security_data.company_name,
        exchange=security_data.exchange,
        sector=security_data.sector,
        industry=security_data.industry,
        country=security_data.country,
        active=security_data.active,
    )

    try:
        return repository.create(security)

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.put(
    "/{symbol}",
    response_model=SecurityResponse,
)
def update_security(
    symbol: str,
    security_data: SecurityUpdate,
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)

    existing_security = repository.get_by_symbol(
        symbol.upper()
    )

    if existing_security is None:
        raise HTTPException(
            status_code=404,
            detail=f"Security '{symbol.upper()}' not found.",
        )

    existing_security.company_name = (
        security_data.company_name
    )
    existing_security.exchange = security_data.exchange
    existing_security.sector = security_data.sector
    existing_security.industry = security_data.industry
    existing_security.country = security_data.country
    existing_security.active = security_data.active

    try:
        return repository.update(
            existing_security
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )

@router.get(
    "/ensure/{symbol}",
    response_model=SecurityResponse,
)
def ensure_security(
    symbol: str,
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)
    ingestor = SecurityIngestor(repository)

    try:
        return ingestor.ingest(symbol)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.delete("/{symbol}")
def delete_security(
    symbol: str,
    db: Session = Depends(get_db),
):
    repository = SecurityRepository(db)

    security = repository.get_by_symbol(
        symbol.upper()
    )

    if security is None:
        raise HTTPException(
            status_code=404,
            detail=f"Security '{symbol.upper()}' not found.",
        )

    repository.delete(security)

    return {
        "message": (
            f"Security '{symbol.upper()}' "
            "deleted successfully."
        )
    }