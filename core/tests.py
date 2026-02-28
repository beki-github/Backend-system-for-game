from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AuthTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_register_success(self):
		resp = self.client.post(
			'/api/register/',
			{'username': 'alice', 'password': 'Str0ng!Pass1', 'email': 'a@example.com'},
			format='json',
		)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data['username'], 'alice')

	def test_register_duplicate_username_returns_400(self):
		User.objects.create_user(username='bob', password='Password123')
		resp = self.client.post(
			'/api/register/',
			{'username': 'bob', 'password': 'AnotherPass1', 'email': 'b@example.com'},
			format='json',
		)
		self.assertEqual(resp.status_code, 400)
		self.assertIn('username', resp.data)

	def test_register_weak_password_returns_400(self):
		resp = self.client.post(
			'/api/register/',
			{'username': 'charlie', 'password': '12345678', 'email': 'c@example.com'},
			format='json',
		)
		self.assertEqual(resp.status_code, 400)
		self.assertIn('password', resp.data)

	def test_login_refresh_and_me_endpoints(self):
		User.objects.create_user(username='den', password='StrongPass1')
		login = self.client.post(
			'/api/login/', {'username': 'den', 'password': 'StrongPass1'}, format='json'
		)
		self.assertEqual(login.status_code, 200)
		self.assertIn('access', login.data)
		self.assertIn('refresh', login.data)

		access = login.data['access']
		refresh = login.data['refresh']

		# access protected endpoint
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		me = self.client.get('/api/me/')
		self.assertEqual(me.status_code, 200)
		self.assertEqual(me.data['username'], 'den')

		# refresh token
		refresh_resp = self.client.post('/api/token/refresh/', {'refresh': refresh}, format='json')
		self.assertEqual(refresh_resp.status_code, 200)
		self.assertIn('access', refresh_resp.data)


class LeaderboardTests(TestCase):
	def setUp(self):
		from .models import Game, PlayerProgress

		self.client = APIClient()
		# create users
		self.u1 = User.objects.create_user(username='player1', password='P@ssword1')
		self.u2 = User.objects.create_user(username='player2', password='P@ssword2')
		# create game
		self.game = Game.objects.create(name='Test Game', description='desc')
		# create progress entries
		PlayerProgress.objects.create(player=self.u1, game=self.game, score=150, level=3)
		PlayerProgress.objects.create(player=self.u2, game=self.game, score=100, level=2)

	def test_leaderboard_includes_player_username_and_order(self):
		url = f'/api/games/{self.game.id}/leaderboard/'
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		data = resp.data
		# Expect two entries ordered by score desc
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 2)
		self.assertEqual(data[0]['player_username'], 'player1')
		self.assertEqual(data[0]['score'], 150)
		self.assertEqual(data[1]['player_username'], 'player2')
		self.assertEqual(data[1]['score'], 100)
