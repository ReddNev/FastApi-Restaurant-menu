from tortoise import models, fields


class Menu(models.Model):
    title = fields.CharField(unique=True, max_length=255)
    description = fields.TextField(default=None, null=True)

    submenu: fields.ReverseRelation['SubMenu']

    async def submenu_count(self) -> int:
        return await self.submenu.all().count()

    async def dish_count(self) -> int:
        return sum([
            await submenu.dish_count()
            for submenu in await self.submenu.all()
        ])


class SubMenu(models.Model):
    title = fields.CharField(unique=True, max_length=255)
    description = fields.TextField(default=None, null=True)
    menu = fields.ForeignKeyField('models.Menu', related_name='submenu', on_delete=fields.CASCADE)

    dishes: fields.ReverseRelation['Dish']

    async def dish_count(self) -> int:
        return await self.dishes.all().count()


class Dish(models.Model):
    title = fields.CharField(unique=True, max_length=255)
    description = fields.TextField(default=None, null=True)
    price = fields.DecimalField(default=0, max_digits=18, decimal_places=2)
    submenu = fields.ForeignKeyField('models.SubMenu', related_name='dishes', on_delete=fields.CASCADE)

