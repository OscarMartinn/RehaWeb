# Generated by Django 3.2.9 on 2022-02-17 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accesoTerapeutas', '0012_auto_20220217_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercicios',
            name='video',
            field=models.FileField(blank=True, help_text='Seleccione el video que quieres asociar al ejercicio. Con el siguiente formato: codigo_ejercicio.mp4', null=True, upload_to='ejercicios', verbose_name='Video'),
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
