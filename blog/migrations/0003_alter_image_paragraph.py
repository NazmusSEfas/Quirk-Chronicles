# Generated by Django 4.1 on 2024-10-09 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_image_paragraph"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="paragraph",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="blog.paragraph",
            ),
        ),
    ]
