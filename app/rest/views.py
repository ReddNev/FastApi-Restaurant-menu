from fastapi import APIRouter

from tortoise import exceptions, transactions

from app.db import models

from .schemas import BodyMenu, ResponseMenu
from .schemas import BodySubMenu, ResponseSubMenu
from .schemas import BodyDish, ResponseDish


router = APIRouter()


@router.post(
    '/menus',
    response_model=ResponseMenu,
    tags=['Menu']
)
async def create_menu(body: BodyMenu):
    menu = await models.Menu.create(**body.dict())
    return ResponseMenu(id=menu.pk, **body.dict())


@router.get(
    '/menus',
    response_model=list[ResponseMenu],
    tags=['Menu']
)
async def get_menus():
    return [
        ResponseMenu(
            id=menu.pk,
            title=menu.title,
            description=menu.description,
            submenuCount=await menu.submenu_count(),
            dishCount=await menu.dish_count()
        )
        for menu in await models.Menu.all()
    ]


@router.get(
    '/menus/{target_menu_id}',
    response_model=ResponseMenu | dict,
    tags=['Menu']
)
async def get_menu(target_menu_id: int):
    try:
        menu = await models.Menu.get(id=target_menu_id)
        return ResponseMenu(
            id=menu.pk,
            title=menu.title,
            description=menu.description,
            submenuCount=await menu.submenu_count(),
            dishCount=await menu.dish_count()
        )
    except exceptions.DoesNotExist:
        return {}


@router.patch(
    '/menus/{target_menu_id}',
    response_model=ResponseMenu | dict,
    tags=['Menu']
)
async def update_menu(target_menu_id: int, body: BodyMenu):
    async with transactions.in_transaction():
        try:
            menu = await models.Menu.get(id=target_menu_id)
        except exceptions.DoesNotExist:
            return {}
        menu.title = body.title or menu.title
        menu.description = body.description or menu.description
        await menu.save()
    return ResponseMenu(
        id=menu.pk,
        title=menu.title,
        description=menu.description,
        submenuCount=await menu.submenu_count(),
        dishCount=await menu.dish_count()
    )


@router.delete(
    '/menus/{target_menu_id}',
    tags=['Menu']
)
async def delete_menu(target_menu_id: int):
    menu = await models.Menu.get_or_none(id=target_menu_id)
    if menu is not None:
        await menu.delete()


@router.post(
    '/menus/{target_menu_id}/submenus',
    response_model=ResponseSubMenu,
    tags=['SubMenu']
)
async def create_submenu(target_menu_id: int, body: BodySubMenu):
    submenu = await models.SubMenu.create(**body.dict(), menu_id=target_menu_id)
    return ResponseSubMenu(
        id=submenu.pk,
        **body.dict(),
        menuId=target_menu_id
    )


@router.get(
    '/menus/{target_menu_id}/submenus',
    response_model=list[ResponseSubMenu],
    tags=['SubMenu']
)
async def get_submenus(target_menu_id: int):
    return [
        ResponseSubMenu(
            id=submenu.pk,
            title=submenu.title,
            description=submenu.description,
            menuId=submenu.menu_id,
            dishCount=await submenu.dish_count()
        )
        for submenu in await models.SubMenu.filter(menu_id=target_menu_id).all()
    ]


@router.get(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}',
    response_model=ResponseSubMenu | dict,
    tags=['SubMenu']
)
async def get_submenu(target_menu_id: int, target_submenu_id: int):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is not None:
        return ResponseSubMenu(
            id=submenu.pk,
            title=submenu.title,
            description=submenu.description,
            menuId=submenu.menu_id,
            dishCount=await submenu.dish_count()
        )
    return {}


@router.patch(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}',
    response_model=ResponseSubMenu | dict,
    tags=['SubMenu']
)
async def update_submenu(target_menu_id: int, target_submenu_id: int, body: BodySubMenu):
    async with transactions.in_transaction():
        submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
        if submenu is None:
            return {}
        submenu.title = body.title or submenu.title
        submenu.description = body.description or submenu.description
        await submenu.save()
    return ResponseSubMenu(
        id=submenu.pk,
        title=submenu.title,
        description=submenu.description,
        menuId=submenu.menu_id,
        dishCount=await submenu.dish_count()
    )


@router.delete(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}',
    tags=['SubMenu']
)
async def delete_submenu(target_menu_id: int, target_submenu_id: int):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is not None:
        await submenu.delete()


@router.post(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    response_model=ResponseDish | dict,
    tags=['Dish']
)
async def create_dish(target_menu_id: int, target_submenu_id: int, body: BodyDish):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is None:
        return {}

    dish = await models.Dish.create(
        **body.dict(),
        submenu_id=submenu.pk
    )
    return ResponseDish(
        id=dish.pk,
        **body.dict(),
        submenuId=target_submenu_id
    )


@router.get(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    response_model=list[ResponseDish],
    tags=['Dish']
)
async def get_dishes(target_menu_id: int, target_submenu_id: int):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is None:
        return []

    return [
        ResponseDish(
            id=dish.pk,
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenuId=dish.submenu_id
        )
        for dish in await models.Dish.filter(submenu_id=submenu.pk).all()
    ]


@router.get(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=ResponseDish | dict,
    tags=['Dish']
)
async def get_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is None:
        return {}

    dish = await models.Dish.filter(submenu_id=submenu.pk, id=target_dish_id).first()
    if dish is None:
        return {}

    return ResponseDish(
        id=dish.pk,
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenuId=dish.submenu_id
    )


@router.patch(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=ResponseDish | dict,
    tags=['Dish']
)
async def update_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int, body: BodyDish):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is None:
        return {}

    async with transactions.in_transaction():
        dish = await models.Dish.filter(submenu_id=submenu.pk, id=target_dish_id).first()
        if dish is None:
            return {}
        dish.title = body.title or dish.title
        dish.description = body.description or dish.description
        dish.price = body.price or dish.price
        await dish.save()

    return ResponseDish(
        id=dish.pk,
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenuId=dish.submenu_id
    )


@router.delete(
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    tags=['Dish']
)
async def delete_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    submenu = await models.SubMenu.filter(menu_id=target_menu_id, id=target_submenu_id).first()
    if submenu is None:
        return {}

    dish = await models.Dish.filter(submenu_id=submenu.pk, id=target_dish_id).first()
    if dish is not None:
        await dish.delete()
