# Generated by Django 5.1.3 on 2024-12-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_cliente_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]