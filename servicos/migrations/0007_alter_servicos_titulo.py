# Generated by Django 5.1.3 on 2024-12-24 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0006_servicos_data_finalizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicos',
            name='titulo',
            field=models.CharField(max_length=50),
        ),
    ]