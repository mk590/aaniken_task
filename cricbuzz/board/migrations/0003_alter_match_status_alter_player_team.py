# Generated by Django 5.0.4 on 2024-04-19 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_team_player_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(default='upcoming', max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='board.team'),
        ),
    ]
