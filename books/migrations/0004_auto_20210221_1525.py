# Generated by Django 3.1.6 on 2021-02-21 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_claim_create_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='book',
        ),
        migrations.AddField(
            model_name='claim',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='books.writer'),
        ),
        migrations.AddField(
            model_name='claim',
            name='claimant',
            field=models.ManyToManyField(blank=True, default=None, related_name='claimants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='claim',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
