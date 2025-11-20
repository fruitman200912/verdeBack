# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Verde Backend is a FastAPI-based geospatial application for tracking species observations using PostGIS. The application uses async SQLAlchemy with PostgreSQL/PostGIS for spatial data queries.

## Development Commands

### Running the Application

```bash
# Using Docker Compose (recommended)
docker-compose up --build

# The API will be available at http://localhost:8000
# PostgreSQL/PostGIS will be available at localhost:5432
```

### Running Without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Database Commands

The application uses PostGIS (PostgreSQL with spatial extensions). The database container includes a health check that retries connection up to 10 times with 5-second intervals.

**Important**: Database initialization happens automatically via the `lifespan` handler in `main.py:47-68`. The retry logic handles initial connection failures when Docker containers start.

## Architecture

### Layered Structure

The codebase follows a clean layered architecture:

1. **API Layer** (`/api/`): FastAPI routers and endpoint definitions
2. **CRUD Layer** (`/cruds/`): Database operations (queries, inserts, updates)
3. **Models Layer** (`/models/`): SQLAlchemy ORM models
4. **Schemas Layer** (`/schemas/`): Pydantic models for request/response validation
5. **Database Layer** (`/database/`): Connection management and session handling

### Model Registration Pattern

**Critical**: All new SQLAlchemy models MUST be imported in `main.py` before database initialization to register them in SQLAlchemy's metadata. Without this, tables won't be created.

```python
# Example from main.py:13-15
from models import species_model
from models import observation_model
# from models import [new_model_file]  # Add new models here
```

### Database Session Management

- Use `get_db_session()` from `database/connection.py` as a FastAPI dependency
- Sessions are async and use `AsyncSession` from SQLAlchemy
- Connection pooling: pool_size=10, max_overflow=20
- All database operations must use `await` and async functions

### Base Model Inheritance

All models should inherit from `BaseModel` (defined in `models/base.py`), which provides:
- `created_at`: Auto-populated timestamp
- `updated_at`: Auto-updated timestamp

Note: `observation_model.py` currently inherits from `Base` directly instead of `BaseModel` - this is an inconsistency.

### Geospatial Data Pattern

The project uses GeoAlchemy2 for PostGIS integration:

```python
from geoalchemy2 import Geometry

# POINT geometry with WGS84 (latitude/longitude)
location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
```

The `Observation` model stores both the PostGIS `location` column and separate `latitude`/`longitude` columns for query convenience.

## Environment Configuration

Database credentials are stored in `.env`:
- `POSTGRES_HOST`: Use "db" for Docker, "localhost" for local
- `POSTGRES_PORT`: 5432
- `POSTGRES_USER`: verde_user
- `POSTGRES_PASSWORD`: V3rd3B@ckendP@ss
- `POSTGRES_DB`: verde_db

The connection string is constructed in `database/connection.py:15-18` using `postgresql+asyncpg://` driver.

## Adding New Features

### Adding a New Model

1. Create model file in `/models/` inheriting from `BaseModel`
2. Import the model in `main.py` (critical for table creation)
3. Create corresponding schema in `/schemas/`
4. Create CRUD functions in `/cruds/`
5. Create endpoint router in `/api/endpoints/`
6. Register router in `/api/api_router.py`

### Adding Endpoints

All endpoints are registered through `api_router.py` with a prefix and tags:

```python
api_router.include_router(species.router, prefix="/species", tags=["species"])
```

Final URL pattern: `/api/{prefix}/{endpoint}`

Example: `/api/species/` for the species list endpoint
