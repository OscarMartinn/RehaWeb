# Generated by Django 3.2.9 on 2022-06-13 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('englishAccess', '0018_auto_20220407_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationsession',
            old_name='finalDate',
            new_name='final_Date',
        ),
        migrations.RenameField(
            model_name='registrationsession',
            old_name='initialDate',
            new_name='initial_Date',
        ),
        migrations.RenameField(
            model_name='sessions',
            old_name='finalDate',
            new_name='final_Date',
        ),
        migrations.RenameField(
            model_name='sessions',
            old_name='initialDate',
            new_name='initial_Date',
        ),
    ]
