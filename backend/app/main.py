from fastapi import FastAPI

from app.api.v1.routes import router as v1_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level)
app = FastAPI(title='AI Call Center SaaS')
app.include_router(v1_router, prefix=settings.api_prefix)
