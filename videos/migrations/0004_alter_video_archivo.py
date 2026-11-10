from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_cambio_rutas_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='archivo',
            field=models.FileField(upload_to='videos/'),
        ),
    ]
