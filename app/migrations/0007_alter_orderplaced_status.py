# Generated by Django 4.1.4 on 2023-08-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel'), ('On The Way', 'On The Way')], default='Pending', max_length=50),
        ),
    ]
