from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='team',
            field=models.ForeignKey(
                to='basic_info.Team',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
                related_name='athletes',
                verbose_name='所属代表队',
            ),
        ),
    ]
