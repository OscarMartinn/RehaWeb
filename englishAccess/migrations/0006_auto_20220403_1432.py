# Generated by Django 3.2.9 on 2022-04-03 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('englishAccess', '0005_auto_20220403_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gmfcsenglish',
            old_name='name',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='macsenglish',
            old_name='name',
            new_name='nombre',
        ),
    ]
