# Generated by Django 3.0.3 on 2020-04-21 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_dataset_tasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('queued', 'Queued for processing'), ('running', 'Processing'), ('internal_failure', 'Internal failure'), ('failed', 'Failed'), ('success', 'Succeeded')], default='queued', max_length=20)),
                ('fail_reason', models.TextField(blank=True)),
                ('algorithm', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Algorithm')),
                ('algorithm_result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.AlgorithmResult')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Dataset')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
