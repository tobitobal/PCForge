# Generated by Django 5.0.1 on 2024-01-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_detallepedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='productos',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('preparacion', 'En preparación'), ('ensamblaje', 'En ensamblaje'), ('en_camino', 'En camino'), ('entregado', 'Entregado')], default='preparacion', max_length=20),
        ),
    ]
