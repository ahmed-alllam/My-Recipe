#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 18:47.

# Generated by Django 3.0.4 on 2020-03-23 16:46

from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_auto_20200323_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=recipes.models.image_upload)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images',
                                             to='recipes.RecipeModel')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ingredientmodel',
            unique_together={('recipe', 'name')},
        ),
        migrations.DeleteModel(
            name='ImageModel',
        ),
        migrations.RemoveField(
            model_name='ingredientmodel',
            name='slug',
        ),
    ]