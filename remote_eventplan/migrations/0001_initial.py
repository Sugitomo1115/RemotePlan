# Generated by Django 3.2.5 on 2021-11-30 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('target', models.CharField(max_length=20)),
                ('person', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=100)),
                ('tools', models.CharField(max_length=100)),
                ('help', models.CharField(max_length=100)),
                ('outline', models.CharField(max_length=200)),
                ('posted_at', models.DateTimeField(verbose_name='date published')),
                ('like', models.IntegerField(default=0)),
            ],
        ),
    ]
