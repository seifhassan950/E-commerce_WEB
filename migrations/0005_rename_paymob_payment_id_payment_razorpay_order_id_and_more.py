# Generated by Django 5.1.4 on 2024-12-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_payment_orderplaced'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='paymob_payment_id',
            new_name='razorpay_order_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='paymob_order_id',
            new_name='razorpay_payment_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paymob_payment_status',
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
