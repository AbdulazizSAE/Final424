# Generated by Django 5.0.1 on 2024-05-16 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('time_to_serve', models.IntegerField(help_text='Time to make and serve in minutes')),
                ('description', models.TextField()),
            ],
        ),
    ]