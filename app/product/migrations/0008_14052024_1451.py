from django.db import migrations
from django.db.migrations import RunPython


def noop(apps, schema_editor):
    pass


def subscription_counts(apps, schema_editor):
    ProductType = apps.get_model('product', 'ProductType')
    data = ['Женщинам', 'Обувь', "Детям", "Мужчинам", "Дом",
            "Красота", "Аксессуары", "Электроника", "Игрушки",
            "Мебель", "Продукты", "Бытовая техника", "Зоотовары",
            "Спорт", "Автотовары", "Книги", "Для ремонта", "Сад и дача",
            "Здоровье", "Канцтовары"]
    for i in data:
        ProductType.objects.create(name=i)


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0007_adminsettings_minimum_quantity_of_goods_and_more'),
    ]

    operations = [
        RunPython(subscription_counts, noop)
    ]
