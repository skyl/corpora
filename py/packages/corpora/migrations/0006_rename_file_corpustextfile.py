# Generated by Django 5.1.2 on 2024-11-03 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("corpora", "0005_alter_corpus_unique_together"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="File",
            new_name="CorpusTextFile",
        ),
    ]
