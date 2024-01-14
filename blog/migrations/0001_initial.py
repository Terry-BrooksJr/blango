# Generated by Django 5.0.1 on 2024-01-14 21:36

import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blog_comments',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Written On')),
                ('last_modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated On')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Posted On')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(unique=True)),
                ('summary', models.TextField(max_length=500)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published'), ('W', 'Withdrawn')], default='D', max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Post Creator')),
            ],
            options={
                'db_table': 'blog_posts',
                'ordering': ['-last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('value', models.TextField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'blog_tags',
                'order_with_respect_to': 'value',
                'indexes': [models.Index(fields=['value'], name='tag_value')],
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(models.OrderBy(django.db.models.functions.text.Lower('value'), descending=True), name='unique_lower_name_tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.tag'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author'], name='post_author'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['status'], name='posts_status'),
        ),
    ]
