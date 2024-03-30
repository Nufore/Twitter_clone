from fastapi import APIRouter

from .users.views import router as users_router
from .tweets.views import router as tweets_router
from .medias.views import router as medias_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=tweets_router, prefix="/tweets")
router.include_router(router=medias_router, prefix="/medias")
