# Generated by Django 2.2.4 on 2019-08-23 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Friend', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='instagram.Posts')),
            ],
        ),
    ]