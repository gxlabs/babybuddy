from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_medication"),
    ]

    operations = [
        migrations.AddField(
            model_name="diaperchange",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="diaperchange/images/",
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="feeding",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="feeding/images/",
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="pumping",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="pumping/images/",
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="sleep",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="sleep/images/",
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="tummytime",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="tummytime/images/",
                verbose_name="Image",
            ),
        ),
    ]
