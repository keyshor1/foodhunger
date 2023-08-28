# Generated by Django 4.1.4 on 2023-08-16 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_alter_orderplaced_status'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('billing_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Credit', 'Credit'), ('Cash', 'Cash'), ('Pending', 'Pending'), ('Online Payment', 'Online Payment')], default='Pending', max_length=50)),
                ('cabin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.cabin')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
