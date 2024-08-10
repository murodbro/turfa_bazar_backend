# Generated by Django 5.0.3 on 2024-06-24 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_email_order_phone_orderitems'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='status',
            field=models.CharField(choices=[('KUTILMOQDA', 'Kutilmoqda...'), ("JO'NATILINMOQDA", "Jo'natilinmoqda..."), ('YETKAZIB BERILDI', 'Yetkazib berildi...'), ('BEKOR QILINDI', 'Bekor qilindi')], default='KUTILMOQDA', max_length=50),
        ),
    ]
