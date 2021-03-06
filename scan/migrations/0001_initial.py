# Generated by Django 2.0.5 on 2018-05-09 23:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=0)),
                ('units', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('amount_purchased', models.FloatField(default=1)),
                ('amount_consumed', models.FloatField(default=0)),
                ('amount_wasted', models.FloatField(default=0)),
                ('percent_wasted', models.FloatField(default=0)),
                ('money_wasted', models.FloatField(default=0)),
                ('money_spent', models.FloatField(default=0)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scan.Food')),
            ],
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('amount', models.FloatField(default=1)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scan.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_spent', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('items', models.ManyToManyField(through='scan.ListItem', to='scan.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('total_money_wasted', models.FloatField(default=0)),
                ('total_percent_wasted', models.FloatField(default=0)),
                ('items', models.ManyToManyField(through='scan.ItemResults', to='scan.Food')),
                ('receipt', models.ManyToManyField(to='scan.Receipt')),
            ],
        ),
        migrations.AddField(
            model_name='listitem',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scan.Receipt'),
        ),
        migrations.AddField(
            model_name='itemresults',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scan.Survey'),
        ),
    ]
