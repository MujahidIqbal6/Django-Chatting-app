# Generated by Django 3.2.7 on 2021-09-16 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_user_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mesg',
            name='user',
        ),
        migrations.AddField(
            model_name='mesg',
            name='from_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sentfrom', to='chat.user'),
        ),
        migrations.AddField(
            model_name='mesg',
            name='to_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sentto', to='chat.user'),
        ),
    ]