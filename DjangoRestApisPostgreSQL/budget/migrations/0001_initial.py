# Generated by Django 4.0.2 on 2022-03-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trans',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transactonDescript', models.CharField(max_length=500)),
                ('amount', models.FloatField()),
                ('transactonDate', models.DateField()),
                ('bankAction', models.CharField(max_length=1)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transactonDescript', models.CharField(max_length=500)),
                ('amount', models.FloatField()),
                ('transactonDate', models.DateField()),
                ('bankAction', models.CharField(max_length=1)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]