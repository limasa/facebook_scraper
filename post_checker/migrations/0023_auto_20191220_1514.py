# Generated by Django 3.0.1 on 2019-12-20 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_checker', '0022_page_page_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='page_id',
            new_name='page_identifier',
        ),
    ]