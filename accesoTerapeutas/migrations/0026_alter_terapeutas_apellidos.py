# Generated by Django 3.2.9 on 2022-04-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accesoTerapeutas', '0025_remove_terapeutas_nombreusuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terapeutas',
            name='apellidos',
            field=models.CharField(help_text='Indique los apellidos del terapeuta.', max_length=20, verbose_name='Apellidos'),
        ),
    ]
