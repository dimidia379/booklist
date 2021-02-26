# Generated by Django 3.1.6 on 2021-02-21 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20210221_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='author',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='title',
        ),
        migrations.AddField(
            model_name='claim',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='claimedBooks', to='books.book'),
        ),
    ]
