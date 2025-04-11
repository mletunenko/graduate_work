from fastapi import APIRouter

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("", summary="Создать профиль пользователя")
async def create_profile():
    pass


@router.get("", summary="Получить список профилей")
async def list_profile():
    pass


@router.get("/{profile_id}", summary="Получить профиль по id")
async def get_profile_by_id():
    pass


@router.patch("/{profile_id}", summary="Обновить профиль пользователя")
async def update_profile():
    pass


@router.delete("/profile_id", summary="Удалить профиль пользователя")
async def delete_profile():
    pass
