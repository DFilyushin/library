from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)


@router.post('')
async def create_user():
    pass


@router.post('/auth')
async def auth():
    pass


@router.post('/logout')
async def logout():
    pass


@router.get('/{login}')
@router.delete('/{login}')
async def user_cabinet(login: str):
    pass
