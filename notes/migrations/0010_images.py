# Generated by Django 4.1.7 on 2023-03-11 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_alter_note_last_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='note_images')),
                ('alt_text', models.CharField(max_length=200)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.note')),
            ],
        ),
    ]
