# Generated by Django 5.0.4 on 2024-04-30 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("character", "0002_alter_character_birth_alter_character_death_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="character",
            old_name="character_id",
            new_name="_id",
        ),
        migrations.RenameField(
            model_name="character",
            old_name="character_name",
            new_name="name",
        ),
    ]