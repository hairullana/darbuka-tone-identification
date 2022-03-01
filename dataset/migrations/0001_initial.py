# Generated by Django 4.0.2 on 2022-03-01 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tone', models.CharField(max_length=16)),
                ('extraction', models.TextField()),
            ],
            options={
                'db_table': 'dataset',
                'managed': False,
            },
        ),
    ]
