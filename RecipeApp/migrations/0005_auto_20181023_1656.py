# Generated by Django 2.1.2 on 2018-10-23 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecipeApp', '0004_recipe_trending_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='avg_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]