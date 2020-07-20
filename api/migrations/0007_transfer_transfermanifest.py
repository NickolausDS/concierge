# Generated by Django 3.0.8 on 2020-07-20 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_upgrade_auth_and_swagger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('submission_id', models.UUIDField()),
                ('task_id', models.UUIDField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('completion_time', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=32)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='transfers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransferManifest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('transfer',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='api.Transfer')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='manifests',
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
