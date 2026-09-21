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


class City(BaseModel):
    name: str
    country_code: str
    country: str
    region: str
    population: int


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


CITIES = [
    City(name="New Delhi", country_code="IN", country="India", region="Asia", population=249998),
    City(name="Mumbai", country_code="IN", country="India", region="Asia", population=12442373),
    City(name="Bengaluru", country_code="IN", country="India", region="Asia", population=8443675),
    City(name="Washington, D.C.", country_code="US", country="United States", region="Americas", population=689545),
    City(name="New York City", country_code="US", country="United States", region="Americas", population=8804190),
    City(name="Los Angeles", country_code="US", country="United States", region="Americas", population=3898747),
    City(name="London", country_code="GB", country="United Kingdom", region="Europe", population=8982000),
    City(name="Manchester", country_code="GB", country="United Kingdom", region="Europe", population=553230),
    City(name="Tokyo", country_code="JP", country="Japan", region="Asia", population=14094034),
    City(name="Osaka", country_code="JP", country="Japan", region="Asia", population=2753862),
    City(name="Canberra", country_code="AU", country="Australia", region="Oceania", population=456692),
    City(name="Sydney", country_code="AU", country="Australia", region="Oceania", population=5312163),
    City(name="Brasília", country_code="BR", country="Brazil", region="Americas", population=2817068),
    City(name="São Paulo", country_code="BR", country="Brazil", region="Americas", population=11451245),
    City(name="Berlin", country_code="DE", country="Germany", region="Europe", population=3644826),
    City(name="Munich", country_code="DE", country="Germany", region="Europe", population=1488202),
    City(name="Pretoria", country_code="ZA", country="South Africa", region="Africa", population=741651),
    City(name="Cape Town", country_code="ZA", country="South Africa", region="Africa", population=433688),
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


@app.get("/cities", response_model=list[City], tags=["cities"])
def list_cities(
    country_code: str | None = Query(default=None, description="Filter by country code, e.g. IN"),
    region: str | None = Query(default=None, description="Filter by region, e.g. Asia"),
) -> list[City]:
    """Return cities filtered by country code, region, or both."""
    results = CITIES
    if country_code:
        results = [city for city in results if city.country_code.casefold() == country_code.casefold()]
    if region:
        results = [city for city in results if city.region.casefold() == region.casefold()]
    return results


@app.get("/countries/{code}", response_model=Country, tags=["countries"])
def get_country(code: str) -> Country:
    for country in COUNTRIES:
        if country.code.casefold() == code.casefold():
            return country
    raise HTTPException(status_code=404, detail=f"Country with code '{code}' was not found")
