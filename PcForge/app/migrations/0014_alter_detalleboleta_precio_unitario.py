# Generated by Django 5.0.1 on 2024-01-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_boleta_detalleboleta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleboleta',
            name='precio_unitario',
            field=models.IntegerField(),
        ),
    ]
