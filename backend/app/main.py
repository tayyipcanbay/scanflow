from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import upload, comparison, insights, actions
from app.database.connection import Base, engine

app = FastAPI(
    title="3D Body Progress Engine API",
    description="API for comparing 3D body meshes over time",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(comparison.router, prefix="/api/comparison", tags=["comparison"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(actions.router, prefix="/api/actions", tags=["actions"])


@app.get("/")
async def root():
    return {"message": "3D Body Progress Engine API"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}

