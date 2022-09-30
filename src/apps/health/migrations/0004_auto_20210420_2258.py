# Generated by Django 3.1.2 on 2021-04-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0003_food_foodid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='calories_per_gram',
        ),
        migrations.AddField(
            model_name='food',
            name='calories',
            field=models.PositiveIntegerField(default=0, verbose_name='Calories'),
        ),
    ]
