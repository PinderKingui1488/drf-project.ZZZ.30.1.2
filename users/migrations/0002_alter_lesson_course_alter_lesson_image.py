import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_alter_lesson_course_alter_lesson_image'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Почта пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Номер телефона'),
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='Дата оплаты')),
                ('payment_amount', models.IntegerField(blank=True, default=0, null=True, verbose_name='Сумма оплаты')),
                ('payment_method', models.CharField(blank=True, choices=[('cash', 'наличные'), ('transfer', 'перевод на счет')], default='cash', max_length=10, null=True, verbose_name='Способ оплаты')),
                ('paid_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='education.course', verbose_name='Оплаченный курс')),
                ('separately_paid_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='education.lesson', verbose_name='Оплаченный урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]