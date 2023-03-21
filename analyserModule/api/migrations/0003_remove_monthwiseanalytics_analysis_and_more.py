# Generated by Django 4.1.7 on 2023-03-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_monthwiseanalytics_phonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthwiseanalytics',
            name='analysis',
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='avgBalance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='avgSpending',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='largeCreditSources',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='largeDebitSources',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='monthlyLoan',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthwiseanalytics',
            name='spendingIncomeRatio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]