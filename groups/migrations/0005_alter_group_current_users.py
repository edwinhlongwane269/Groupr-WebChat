# Generated by Django 4.2 on 2023-04-23 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_groupattendee_user_groupattendee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='current_users',
            field=models.ManyToManyField(blank=True, related_name='attendants-rooms+', to='groups.groupattendee'),
        ),
    ]