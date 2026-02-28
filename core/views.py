from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import (
    Game,
    PlayerProgress,
    Achievement,
    PlayerAchievement,
)
from .serializers import (
    RegisterSerializer,
    MeSerializer,
    GameSerializer,
    PlayerProgressSerializer,
    AchievementSerializer,
    PlayerAchievementSerializer,
)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(MeSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = MeSerializer(request.user)
    return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminUser]

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[AllowAny],
    )
    def leaderboard(self, request, pk=None):
        game = self.get_object()
        queryset = PlayerProgress.objects.filter(game=game).order_by("-score")
        serializer = PlayerProgressSerializer(queryset, many=True)
        return Response(serializer.data)


class PlayerProgressViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayerProgress.objects.filter(player=self.request.user)

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAdminUser]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlock_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    player_achievement, created = PlayerAchievement.objects.get_or_create(
        player=request.user,
        achievement=achievement,
    )
    serializer = PlayerAchievementSerializer(player_achievement)
    status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=status_code)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_achievements(request):
    queryset = PlayerAchievement.objects.filter(player=request.user)
    serializer = PlayerAchievementSerializer(queryset, many=True)
    return Response(serializer.data)
