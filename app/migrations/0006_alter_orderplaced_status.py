# Generated by Django 4.1.4 on 2023-08-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('On The Way', 'On The Way'), ('Packed', 'Packed'), ('Accepted', 'Accepted')], default='Pending', max_length=50),
        ),
    ]
