# Generated by Django 3.2.9 on 2022-03-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_eventplan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='なし', max_length=30, unique=True)),
            ],
        ),
    ]