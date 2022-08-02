# Generated by Django 4.0.6 on 2022-08-02 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_remove_profile_id_remove_profile_spicies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='nickname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.profile'),
        ),
        migrations.AlterField(
            model_name='board',
            name='nickname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.profile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='nickname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.profile'),
        ),
    ]
