# Countries API

A small Python project built with [FastAPI](https://fastapi.tiangolo.com/) for listing and looking up country details.

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>.

Interactive API documentation:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Endpoints

- `GET /health` — health check
- `GET /countries` — list all countries
- `GET /countries?region=Asia` — filter by region
- `GET /countries?search=india` — search by name, capital, or ISO code
- `GET /countries/IN` — get one country by its code

Example:

```bash
curl http://127.0.0.1:8000/countries/IN
```
