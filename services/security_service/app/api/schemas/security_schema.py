from pydantic import BaseModel, ConfigDict


class SecurityCreate(BaseModel):
    symbol: str
    company_name: str
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    active: bool = True


class SecurityUpdate(BaseModel):
    company_name: str
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    active: bool = True


class SecurityResponse(BaseModel):
    id: int
    symbol: str
    company_name: str
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    active: bool

    model_config = ConfigDict(from_attributes=True)