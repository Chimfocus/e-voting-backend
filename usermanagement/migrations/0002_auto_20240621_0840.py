# Generated by Django 3.2.12 on 2024-06-21 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('campus_name', models.CharField(max_length=255)),
                ('campus_location', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='campus',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usermanagement.campus'),
        ),
    ]
