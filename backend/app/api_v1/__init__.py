from fastapi import APIRouter
from .users.views import router as user_router
from .auth.views import router as auth_router
from .lots.views import router as lot_router
from .bids.view import router as bid_router

router = APIRouter()

router.include_router(
    router=user_router,
    prefix="/user",
)
router.include_router(
    router=auth_router,
    prefix="/auth",
)

router.include_router(
    router=lot_router,
    prefix="/lot",
)

router.include_router(
    router=bid_router,
    prefix="/bid",
)
