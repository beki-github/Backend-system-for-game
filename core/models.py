from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class PlayerProgress(models.Model):
    player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_progress"
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="player_progress"
    )
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    class Meta:
        unique_together = ("player", "game")

    def __str__(self) -> str:
        return f"{self.player.username} - {self.game.name}"


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="achievements"
    )

    class Meta:
        unique_together = ("name", "game")

    def __str__(self) -> str:
        return f"{self.name} ({self.game.name})"


class PlayerAchievement(models.Model):
    player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_achievements"
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name="player_achievements"
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("player", "achievement")

    def __str__(self) -> str:
        return f"{self.player.username} - {self.achievement.name}"

