# Generated by Django 4.0.2 on 2022-03-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0016_remove_employee_actual_working_hour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic_inf',
            name='test',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
