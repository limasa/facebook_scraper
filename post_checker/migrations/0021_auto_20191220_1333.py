# Generated by Django 3.0.1 on 2019-12-20 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_checker', '0020_auto_20191220_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='page_author',
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]