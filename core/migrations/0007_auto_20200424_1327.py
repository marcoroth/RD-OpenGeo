# Generated by Django 3.0.3 on 2020-04-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200424_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithmresult',
            name='log',
            field=models.FileField(blank=True, null=True, upload_to='results_logs'),
        ),
    ]
