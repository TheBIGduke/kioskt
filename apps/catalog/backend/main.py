# Made by Kaléin Tamaríz
import os
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from apps.catalog.routers import router as catalog_router
from repositories import MockRepository
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(title="Products and Surveys Catalog")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

from fastapi import Request
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

BASE_MEDIA_URL = os.getenv("BASE_MEDIA_URL", "/media")
DB_URL = os.getenv("DATABASE_URL")

use_sql = False
db_error = None
if DB_URL:
    try:
        from db import SessionLocal
        from apps.catalog.models import Product, Category, ProductMedia
        if SessionLocal:
            with SessionLocal() as db_session:
                # Query the first product
                first_product = db_session.query(Product).first()
                # Test the other tables to ensure schema is fully correct
                db_session.query(Category).first()
                db_session.query(ProductMedia).first()
                
                if first_product is None:
                    logger.info("Database is properly formatted but empty. Falling back to mock data.")
                    use_sql = False
                else:
                    use_sql = True
    except Exception as e:
        db_error = str(e)
        logger.warning(f"Database format mismatch or connection error: {db_error}. Falling back to mock data.")
        use_sql = False

if use_sql:
    # Use the external media path when connected to the database
    IMG_PATH = os.path.expanduser(os.getenv("EXTERNAL_IMAGE_PATH", "./"))
    app.include_router(catalog_router)
else:
    # Fallback to MockRepository and local media
    logger.info("Using local media fallback from frontend/media/products")
    IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/media/products"))
    repo = MockRepository(BASE_MEDIA_URL)
    
    @app.get("/api/categories")
    def get_cats(): return repo.get_categories()

    @app.get("/api/products")
    def get_prods(category_id: int = Query(None)): return repo.get_products(category_id)

if use_sql:
    IMG_PATH = os.path.expanduser(os.getenv("EXTERNAL_IMAGE_PATH", "./"))
    AUDIO_PATH = os.path.expanduser(os.getenv("EXTERNAL_AUDIO_PATH", "/home/thebigduke/productsandsurveys_dashboard_back/media/audios"))
else:
    IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/media/products"))
    AUDIO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/media/audios"))

@app.get("/api/db-status")
def get_db_status():
    return {"status": "connected" if use_sql else "fallback", "error": db_error}

# Mount the Folder (after determining source)
app.mount("/media", StaticFiles(directory=IMG_PATH), name="media")
app.mount("/audio-assets", StaticFiles(directory=AUDIO_PATH), name="audio")

# Mount the frontend application
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)