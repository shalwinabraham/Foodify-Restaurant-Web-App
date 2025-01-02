# Generated by Django 5.1.3 on 2024-12-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0005_alter_fooditem_image_alter_cartitem_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='foodapp.fooditem'),
        ),
    ]