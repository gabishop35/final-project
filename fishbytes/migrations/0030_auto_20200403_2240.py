# Generated by Django 3.0.5 on 2020-04-03 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fishbytes', '0029_auto_20200403_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catch',
            name='lake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fishbytes.Lake'),
        ),
    ]
