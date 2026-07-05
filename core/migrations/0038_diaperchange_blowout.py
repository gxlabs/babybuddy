from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0037_event_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="diaperchange",
            name="blowout",
            field=models.BooleanField(
                default=False,
                verbose_name="Blowout",
            ),
        ),
    ]
