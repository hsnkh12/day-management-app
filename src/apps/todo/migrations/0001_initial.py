# Generated by Django 3.1.2 on 2021-03-28 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20210321_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('started', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
                ('rate', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'verbose_name': 'Day Tasks',
                'verbose_name_plural': 'Days Tasks',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, verbose_name='Task')),
                ('time', models.TimeField(blank=True, help_text='Optional', null=True)),
                ('important', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('random', models.BooleanField(default=False)),
                ('day_tasks', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todo.daytasks', verbose_name='Day tasks')),
                ('user_random', models.ForeignKey(blank=True, help_text='If task is random', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='accounts.user', verbose_name='Random task for user')),
            ],
        ),
    ]