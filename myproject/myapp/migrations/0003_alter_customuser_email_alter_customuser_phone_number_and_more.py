# Generated by Django 5.0.2 on 2024-02-19 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/dzdlxfeee/image/upload/v1708327888/weudruemw5fejuoqnnqo.png', null=True, upload_to='profile_pictures'),
        ),
    ]
