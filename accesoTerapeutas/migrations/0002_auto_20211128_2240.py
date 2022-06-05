# Generated by Django 3.2.9 on 2021-11-28 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accesoTerapeutas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacientes',
            name='email',
            field=models.EmailField(default='prueba@mail.es', help_text='Correo electróncio.', max_length=30, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='pacientes',
            name='telefono',
            field=models.CharField(default='000', help_text='Número de teléfono.', max_length=10, verbose_name='Telefono'),
        ),
    ]
