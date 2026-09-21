from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


class Country(BaseModel):
    code: str
    name: str
    capital: str
    region: str
    population: int
    currency: str
    languages: list[str]


COUNTRIES = [
    Country(code="IN", name="India", capital="New Delhi", region="Asia", population=1428627663, currency="Indian rupee", languages=["Hindi", "English"]),
    Country(code="US", name="United States", capital="Washington, D.C.", region="Americas", population=339996563, currency="United States dollar", languages=["English"]),
    Country(code="GB", name="United Kingdom", capital="London", region="Europe", population=67736802, currency="Pound sterling", languages=["English"]),
    Country(code="JP", name="Japan", capital="Tokyo", region="Asia", population=123294513, currency="Japanese yen", languages=["Japanese"]),
    Country(code="AU", name="Australia", capital="Canberra", region="Oceania", population=26439111, currency="Australian dollar", languages=["English"]),
    Country(code="BR", name="Brazil", capital="Brasília", region="Americas", population=216422446, currency="Brazilian real", languages=["Portuguese"]),
    Country(code="DE", name="Germany", capital="Berlin", region="Europe", population=83294633, currency="Euro", languages=["German"]),
    Country(code="ZA", name="South Africa", capital="Pretoria", region="Africa", population=60414495, currency="South African rand", languages=["English", "Afrikaans", "Zulu"]),
]

app = FastAPI(
    title="Countries API",
    description="A simple FastAPI service for browsing country details.",
    version="1.0.0",
)


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"message": "Welcome to the Countries API", "docs": "/docs"}


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/countries", response_model=list[Country], tags=["countries"])
def list_countries(
    region: str | None = Query(default=None, description="Filter by region, e.g. Asia"),
    search: str | None = Query(default=None, description="Search by country name, capital, or code"),
) -> list[Country]:
    results = COUNTRIES
    if region:
        results = [country for country in results if country.region.casefold() == region.casefold()]
    if search:
        term = search.casefold()
        results = [
            country
            for country in results
            if term in country.name.casefold()
            or term in country.capital.casefold()
            or term == country.code.casefold()
        ]
    return results


@app.get("/countries/{code}", response_model=Country, tags=["countries"])
def get_country(code: str) -> Country:
    for country in COUNTRIES:
        if country.code.casefold() == code.casefold():
            return country
    raise HTTPException(status_code=404, detail=f"Country with code '{code}' was not found")
