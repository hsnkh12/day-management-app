# Generated by Django 3.1.2 on 2021-04-19 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_auto_20210417_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='foodId',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]