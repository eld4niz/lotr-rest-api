# Generated by Django 5.0.4 on 2024-05-01 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("character", "0003_rename_character_id_character__id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="character",
            name="wikiUrl",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
