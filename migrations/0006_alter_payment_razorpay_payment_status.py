# Generated by Django 5.1.4 on 2024-12-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_rename_paymob_payment_id_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='razorpay_payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
