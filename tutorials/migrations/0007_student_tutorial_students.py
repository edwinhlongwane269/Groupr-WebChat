# Generated by Django 4.2 on 2023-04-22 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutorials', '0006_alter_tutorial_description_alter_tutorial_lesson_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutorial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tutorial',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='attendees+', to='tutorials.student'),
        ),
    ]
