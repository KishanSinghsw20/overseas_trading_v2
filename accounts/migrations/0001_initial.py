# Generated by Django 4.2.7 on 2025-05-04 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLoc',
            fields=[
                ('branch', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('badd', models.CharField(max_length=255)),
                ('bph', models.CharField(max_length=20)),
                ('baltph', models.CharField(blank=True, max_length=20, null=True)),
                ('bmname', models.CharField(max_length=100)),
                ('bfax', models.CharField(blank=True, max_length=20, null=True)),
                ('bmemail', models.CharField(max_length=100)),
                ('bloc', models.CharField(max_length=100)),
                ('terminus', models.CharField(max_length=100)),
                ('bpassw', models.CharField(max_length=100)),
                ('buname', models.CharField(max_length=100)),
                ('tdet', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Company Location',
                'verbose_name_plural': 'Company Locations',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('supname', models.CharField(max_length=100)),
                ('supadd', models.CharField(max_length=255)),
                ('sph', models.CharField(max_length=20)),
                ('saltph', models.CharField(blank=True, max_length=20, null=True)),
                ('sfax', models.CharField(blank=True, max_length=20, null=True)),
                ('scper', models.CharField(max_length=100)),
                ('scperdesig', models.CharField(max_length=100)),
                ('compemail', models.CharField(max_length=100)),
                ('suname', models.CharField(max_length=100)),
                ('spass', models.CharField(max_length=100)),
                ('sregdt', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('noticeid', models.AutoField(primary_key=True, serialize=False)),
                ('ndt', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.companyloc')),
            ],
            options={
                'verbose_name': 'Notice',
                'verbose_name_plural': 'Notices',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('cltid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=100)),
                ('cpass', models.CharField(max_length=100)),
                ('cadd', models.CharField(max_length=255)),
                ('cph', models.CharField(max_length=20)),
                ('cphalt', models.CharField(blank=True, max_length=20, null=True)),
                ('cfax', models.CharField(blank=True, max_length=20, null=True)),
                ('ccperson', models.CharField(max_length=100)),
                ('cdesig', models.CharField(max_length=100)),
                ('cemail', models.CharField(max_length=100)),
                ('cregdt', models.DateField(auto_now_add=True)),
                ('btype', models.CharField(max_length=50)),
                ('profile', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
    ]
