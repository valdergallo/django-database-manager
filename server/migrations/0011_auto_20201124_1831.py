# Generated by Django 3.1.3 on 2020-11-24 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0010_auto_20201124_1751"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="connectionkeys",
            options={"verbose_name_plural": "Connection Keys"},
        ),
        migrations.DeleteModel(
            name="ServerGroup",
        ),
    ]
