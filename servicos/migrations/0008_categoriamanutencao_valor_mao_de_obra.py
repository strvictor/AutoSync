# Generated by Django 5.1.3 on 2024-12-26 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0007_alter_servicos_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriamanutencao',
            name='valor_mao_de_obra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
