# Generated by Django 3.1.3 on 2020-11-07 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20201107_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='storage_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.uploadstorageconfig'),
        ),
    ]