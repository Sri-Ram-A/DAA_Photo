# Generated by Django 5.2 on 2025-07-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_posts_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='meta',
            field=models.CharField(default='{}'),
        ),
    ]
