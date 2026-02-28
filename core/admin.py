from django.contrib import admin

from .models import Game, PlayerProgress, Achievement, PlayerAchievement


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "game", "score", "level")
    list_filter = ("game",)
    search_fields = ("player__username", "game__name")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "game")
    list_filter = ("game",)
    search_fields = ("name", "game__name")


@admin.register(PlayerAchievement)
class PlayerAchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "achievement", "unlocked_at")
    list_filter = ("achievement__game",)
    search_fields = ("player__username", "achievement__name")

