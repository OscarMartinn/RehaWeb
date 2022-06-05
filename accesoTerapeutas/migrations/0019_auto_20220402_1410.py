# Generated by Django 3.2.9 on 2022-04-02 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accesoTerapeutas', '0018_pci_english_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idiomas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lenguage', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='ejercicios',
            name='english_description',
            field=models.TextField(blank=True, help_text='If you wish, add an explanatory description.', max_length=500, null=True, verbose_name='Descripción en inglés'),
        ),
        migrations.AlterField(
            model_name='ejercicios',
            name='english_name',
            field=models.CharField(blank=True, help_text='Set the name of the new exercise.', max_length=40, null=True, verbose_name='Nombre en inglés'),
        ),
        migrations.AddField(
            model_name='terapeutas',
            name='idioma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accesoTerapeutas.idiomas'),
        ),
    ]
