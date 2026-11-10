from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='archivo',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]
