# Generated by Django 3.1.7 on 2024-06-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='client_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=300)),
                ('client_id', models.CharField(max_length=300)),
                ('tender_location', models.CharField(max_length=300)),
            
            ],
        ),
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_location', models.CharField(max_length=300)),
                ('e_published_date', models.CharField(max_length=300)),
                ('closing_date', models.CharField(max_length=300)),
                ('opening_date', models.CharField(max_length=300)),
                ('title_ref_no', models.CharField(max_length=255, verbose_name='Title and Ref.No./Tender ID')),
                ('organisation_chain', models.CharField(max_length=255, verbose_name='Organisation Chain')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Insert Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
        ),
    ]
