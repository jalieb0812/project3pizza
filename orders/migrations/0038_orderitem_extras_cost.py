# Generated by Django 2.2.10 on 2020-05-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0037_orderitem_extras'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='extras_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]
