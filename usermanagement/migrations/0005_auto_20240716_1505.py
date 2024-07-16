# Generated by Django 3.2.12 on 2024-07-16 15:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0004_user_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredStudents',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student_registration_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='userotps',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 7, 16, 15, 5, 16, 269131, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
