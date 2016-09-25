# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0006_auto_20160623_1627'),
        ('aldryn_people', '0018_auto_20160802_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('address', models.TextField(verbose_name='address', blank=True)),
                ('postal_code', models.CharField(verbose_name='postal code', max_length=20, blank=True)),
                ('city', models.CharField(verbose_name='city', max_length=255, blank=True)),
                ('phone', models.CharField(null=True, verbose_name='phone', max_length=100, blank=True)),
                ('fax', models.CharField(null=True, verbose_name='fax', max_length=100, blank=True)),
                ('email', models.EmailField(verbose_name='email', default='', max_length=254, blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('phone', models.CharField(null=True, verbose_name='phone', max_length=100, blank=True)),
                ('mobile', models.CharField(null=True, verbose_name='mobile', max_length=100, blank=True)),
                ('fax', models.CharField(null=True, verbose_name='fax', max_length=100, blank=True)),
                ('email', models.EmailField(verbose_name='email', default='', max_length=254, blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('description', djangocms_text_ckeditor.fields.HTMLField(verbose_name='description', default='', blank=True)),
                ('visual', filer.fields.image.FilerImageField(null=True, to='filer.Image', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='address',
        ),
        migrations.RemoveField(
            model_name='group',
            name='city',
        ),
        migrations.RemoveField(
            model_name='group',
            name='email',
        ),
        migrations.RemoveField(
            model_name='group',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='group',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='group',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='group',
            name='website',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.RemoveField(
            model_name='person',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='person',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='person',
            name='visual',
        ),
        migrations.RemoveField(
            model_name='person',
            name='website',
        ),
        migrations.RemoveField(
            model_name='persontranslation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='persontranslation',
            name='function',
        ),
        migrations.AddField(
            model_name='group',
            name='profile',
            field=models.OneToOneField(to='aldryn_people.GroupProfile', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='profile',
            field=models.OneToOneField(to='aldryn_people.PersonProfile', default=0),
            preserve_default=False,
        ),
    ]
