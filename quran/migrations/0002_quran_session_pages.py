from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quransession',
            name='ayah_end',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='quransession',
            name='ayah_start',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='quransession',
            name='ayah_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='quransession',
            name='surah_name',
            field=models.CharField(default='Mushaf', max_length=80),
        ),
        migrations.AlterField(
            model_name='quransession',
            name='surah_number',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='QuranSessionPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('para_number', models.PositiveSmallIntegerField(help_text='Juz / para 1–30')),
                ('page_number', models.PositiveSmallIntegerField(help_text='Page within the para PDF (1-based)')),
                ('note', models.TextField(blank=True)),
                ('highlights', models.JSONField(blank=True, default=list, help_text='List of {x,y,w,h,color} with x/y/w/h as fractions of the page (0–1).')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_markups', to='quran.quransession')),
            ],
            options={
                'ordering': ['para_number', 'page_number'],
                'unique_together': {('session', 'para_number', 'page_number')},
            },
        ),
    ]
