# Generated by Django 4.1.4 on 2023-08-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel'), ('Pending', 'Pending'), ('On The Way', 'On The Way'), ('Packed', 'Packed')], default='Pending', max_length=50),
        ),
    ]
