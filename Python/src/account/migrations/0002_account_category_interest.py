# Generated by Django 2.2.2 on 2020-08-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='category_interest',
            field=models.CharField(choices=[('games', 'GAMES'), ('social', 'SOCIAL'), ('music', 'MUSIC'), ('news', 'NEWS')], default='NEWS', max_length=20),
        ),
    ]
