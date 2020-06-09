# Generated by Django 2.2.10 on 2020-05-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0035_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='num_extras',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]