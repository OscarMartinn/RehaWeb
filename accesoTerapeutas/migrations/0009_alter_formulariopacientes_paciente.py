# Generated by Django 3.2.9 on 2021-12-17 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accesoTerapeutas', '0008_auto_20211217_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulariopacientes',
            name='paciente',
            field=models.ForeignKey(blank=True, help_text='Seleccione el paciente', null=True, on_delete=django.db.models.deletion.CASCADE, to='accesoTerapeutas.pacientes', verbose_name='Paciente'),
        ),
    ]
