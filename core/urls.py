from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    register,
    me,
    LoginView,
    RefreshTokenView,
    GameViewSet,
    PlayerProgressViewSet,
    AchievementViewSet,
    unlock_achievement,
    my_achievements,
)

router = DefaultRouter()
router.register("games", GameViewSet, basename="game")
router.register("progress", PlayerProgressViewSet, basename="progress")
router.register("achievements", AchievementViewSet, basename="achievement")

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("me/", me, name="me"),
    path(
        "achievements/unlock/<int:achievement_id>/",
        unlock_achievement,
        name="unlock_achievement",
    ),
    path("my-achievements/", my_achievements, name="my_achievements"),
    path("", include(router.urls)),
]