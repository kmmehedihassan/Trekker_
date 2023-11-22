# Generated by Django 3.2.10 on 2022-11-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0011_alter_mytourinfo_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_id', models.IntegerField()),
                ('guest', models.CharField(max_length=50)),
                ('ticket', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('cardata', models.IntegerField(default=0)),
            ],
        ),
    ]