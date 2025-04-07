import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='education.course', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение'),
        ),
    ]