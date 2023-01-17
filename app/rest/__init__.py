from fastapi import APIRouter

from .views import router as _router


router = APIRouter()
router.include_router(_router)
