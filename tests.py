from dataclasses import fields
from django.test import TestCase
from movies.models import Genre, Movie, Review
from users.models import User
from users.serializers import RegisterSerializer
from django.db.models import EmailField, fields
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class Test(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()

        cls.critic_1_data = {
            "email": "chrys@s.com",
            "username": "chrys",
            "password": "123",
            "first_name": "chrys",
            "last_name": "tian",
            "birthdate": "1999-09-05",
            "bio": "",
            "is_critic": True,
        }

        cls.critic_1_login = {
            "username": "chrys",
            "password": "123",
        }

        cls.user_atributes = {
            "email": "ag@nes.com",
            "username": "agnes",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": False,
        }

        cls.user_data = {
            "email": "a@s.com",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": False,
        }

        cls.wrong_user_data = {
            "email": "a",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "11",
            "bio": "s",
            "is_critic": True,
        }

        cls.duplicate_user_data = {
            "email": "a@s.com",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": True,
        }

        cls.url_post = "/api/users/register/"
        cls.url_login = "/api/users/login/"

        cls.user = User.objects.create(**cls.user_atributes)
        cls.serializer = RegisterSerializer(instance=cls.user)

    def test_contains_expected_fields_serializer(self):
        email_field = User._meta.get_field("email")

        self.assertTrue(isinstance(email_field, EmailField))

    def test_contains_expected_attributes_serializer(self):
        data = self.serializer.data

        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "birthdate",
                    "bio",
                    "is_critic",
                    "updated_at",
                    "is_superuser",
                ]
            ),
        )

    def test_has_expected_fields(self):

        self.assertIsInstance(User._meta.get_field("birthdate"), fields.DateField)
        self.assertIsInstance(User._meta.get_field("email"), fields.EmailField)
        self.assertIsInstance(User._meta.get_field("id"), fields.IntegerField)
        self.assertIsInstance(User._meta.get_field("is_critic"), fields.BooleanField)
        self.assertIsInstance(User._meta.get_field("updated_at"), fields.DateTimeField)
        self.assertIsInstance(User._meta.get_field("is_superuser"), fields.BooleanField)
        self.assertIsInstance(User._meta.get_field("username"), fields.CharField)
        self.assertIsInstance(User._meta.get_field("password"), fields.CharField)
        self.assertIsInstance(User._meta.get_field("first_name"), fields.CharField)
        self.assertIsInstance(User._meta.get_field("last_name"), fields.CharField)


class Test_view(APITestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()

        cls.critic_1_data = {
            "email": "chrys@s.com",
            "username": "chrys",
            "password": "123",
            "first_name": "chrys",
            "last_name": "tian",
            "birthdate": "1999-09-05",
            "bio": "",
            "is_critic": True,
        }

        cls.critic_1_login = {
            "username": "chrys",
            "password": "123",
        }

        cls.admin_data = {
            "email": "lu@cira.com",
            "username": "lucira",
            "password": "123",
            "first_name": "lu",
            "last_name": "cira",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": False,
            "is_superuser": True,
        }

        cls.regular_user_data = {
            "email": "ag@nes.com",
            "username": "agnes",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": False,
        }

        cls.regular_user_data_2 = {
            "email": "a@s.com",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": False,
        }

        cls.wrong_user_data = {
            "email": "a",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "11",
            "bio": "s",
            "is_critic": True,
        }

        cls.duplicate_user_data = {
            "email": "a@s.com",
            "username": "agn",
            "password": "123",
            "first_name": "agnes",
            "last_name": "rosa",
            "birthdate": "1999-09-05",
            "bio": "s",
            "is_critic": True,
        }

        cls.movie_data_1 = {
            "title": "Cowboy bepop",
            "premiere": "1998-01-01",
            "duration": "20min",
            "classification": 16,
            "synopsis": "Spike is a cowboy that eats too much",
            "genres": [{"name": "anime"}],
        }

        cls.movie_data_2 = {
            "title": "Inception",
            "premiere": "1998-01-01",
            "duration": "180min",
            "classification": 16,
            "synopsis": "Where are we",
            "genres": [{"name": "confusion"}],
        }

        cls.movie_data_no_genre_1 = {
            "title": "Cowboy bepop",
            "premiere": "1998-01-01",
            "duration": "20min",
            "classification": 16,
            "synopsis": "Spike is a cowboy that eats too much",
        }

        cls.movie_data_no_genre_2 = {
            "title": "Bebop Cowpoy",
            "premiere": "1998-01-01",
            "duration": "20min",
            "classification": 16,
            "synopsis": "Spike is a cowboy that eats too much",
        }

        cls.review_1_movie_1 = {
            "stars": 10,
            "review": "good soup",
            "spoilers": False,
            "recomendation": "Must Watch",
        }

        cls.review_too_many_stars = {
            "stars": 1000,
            "review": "not very nice soup",
            "spoilers": False,
            "recomendation": "Must Watch",
        }

        cls.url_post = "/api/users/register/"
        cls.url_login = "/api/users/login/"

        cls.user = User.objects.create(**cls.regular_user_data)
        cls.serializer = RegisterSerializer(instance=cls.user)

    def test_create_user_201(self):

        response = self.client.post(
            self.url_post, self.regular_user_data_2, format="json"
        )

        self.assertEquals(201, response.status_code)
        self.assertIn("updated_at", response.json())
        self.assertIn("id", response.json())

    def test_create_user_duplicate_400(self):
        self.user = User.objects.create(**self.regular_user_data_2)

        response = self.client.post(
            self.url_post, self.duplicate_user_data, format="json"
        )

        self.assertEquals(400, response.status_code)
        self.assertIn("username already exists", response.data["username"])
        self.assertIn("email already exists", response.data["email"])

    def test_create_user_without_keys_400(self):
        required_keys = {
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "birthdate",
        }
        response = self.client.post(self.url_post, {}, format="json")

        self.assertEquals(400, response.status_code)

        for key in required_keys:
            self.assertIn("This field is required.", response.data[key])

    def test_create_user_invalid_key_type(self):
        invalid_types = {
            "email": 123,
            "username": 123,
            "password": 123,
            "first_name": 123,
            "last_name": 123,
            "birthdate": 123,
            "bio": 123,
            "is_critic": 123,
        }

        response = self.client.post(self.url_post, invalid_types, format="json")

        self.assertEquals(400, response.status_code)

    def test_login_critic(self):

        critic_1 = User.objects.create_user(**self.critic_1_data)

        response = self.client.post(self.url_login, self.critic_1_login)

        self.assertEqual(critic_1.auth_token.key, response.data["token"])

    def test_non_owner_patch_403(self):
        user_1 = User.objects.create_user(**self.regular_user_data_2)
        critic_1 = User.objects.create_user(**self.critic_1_data)

        user_1_token = Token.objects.create(user=user_1)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_1_token.key)

        response = self.client.get(f"/api/users/{critic_1.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ##### Movies #####

    def test_created_movie_has_expected_fields_201(self):
        admin_user = User.objects.create(**self.admin_data)

        admin_user_token = Token.objects.create(user=admin_user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + admin_user_token.key)

        response = self.client.post("/api/movies/", self.movie_data_1, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("genres", response.data)
        self.assertIn("id", response.data["genres"][0])

    def test_create_movie_regular_user_403(self):

        user_token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_token.key)

        response = self.client.post("/api/movies/", self.movie_data_1, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_movie_critic_user_403(self):
        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response = self.client.post("/api/movies/", self.movie_data_1, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_movie_null_token_401(self):
        response = self.client.post("/api/movies/", self.movie_data_1, format="json")

        self.assertEqual(response.status_code, 401)

    def test_list_movies_200(self):

        genre = Genre.objects.create(**{"name": "anime"})

        movie1 = Movie.objects.create(**self.movie_data_no_genre_1)
        movie2 = Movie.objects.create(**self.movie_data_no_genre_2)

        movie1.genres.add(genre)
        movie2.genres.add(genre)

        response = self.client.get("/api/movies/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertIn("title", response.data["results"][0])
        self.assertIn("id", response.data["results"][0]["genres"][0])

    def test_list_specific_movie_200(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        response = self.client.get(f"/api/movies/{movie.id}/")

        self.assertEqual(response.status_code, 200)

    def test_list_movie_unexintent_404(self):
        response = self.client.get(f"/api/movies/1000/")

        self.assertEqual(response.status_code, 404)

    def test_delete_movie_admin_204(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        admin_user = User.objects.create(**self.admin_data)

        admin_user_token = Token.objects.create(user=admin_user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + admin_user_token.key)

        response = self.client.delete(f"/api/movies/{movie.id}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_movie_regular_user_403(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        user_token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_token.key)

        response = self.client.delete(f"/api/movies/{movie.id}/")

        self.assertEqual(response.status_code, 403)

    def test_delete_movie_critic_403(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response = self.client.delete(f"/api/movies/{movie.id}/")

        self.assertEqual(response.status_code, 403)

    def test_update_movie_superuser_200(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie1 = Movie.objects.create(**self.movie_data_no_genre_1)

        movie1.genres.add(genre)

        admin_user = User.objects.create(**self.admin_data)

        admin_user_token = Token.objects.create(user=admin_user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + admin_user_token.key)

        response = self.client.patch(
            f"/api/movies/{movie1.id}/", self.movie_data_2, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.movie_data_2["title"])

    def test_update_movie_regular_user_403(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie1 = Movie.objects.create(**self.movie_data_no_genre_1)

        movie1.genres.add(genre)

        user_token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_token.key)

        response = self.client.patch(
            f"/api/movies/{movie1.id}/", self.movie_data_2, format="json"
        )

        self.assertEqual(response.status_code, 403)

    ###### Reviews ######

    def test_create_review_critic_201(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertIn("id", response.data)
        self.assertIn("movie_id", response.data)
        self.assertIn("critic", response.data)

    def test_create_review_regular_user_403(self):
        movie_data = {
            "title": "Cowboy bepop",
            "premiere": "1998-01-01",
            "duration": "20min",
            "classification": 16,
            "synopsis": "Spike is a cowboy that eats too much",
        }

        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**movie_data)

        movie.genres.add(genre)

        user_token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_token.key)

        response = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_create_duplicate_review_401(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response1 = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        response2 = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response2.status_code, 401)

    def test_create_review_invalid_start_400(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_too_many_stars,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("stars", response.data)

    def test_list_specific_review_critic_owner_200(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        critic = User.objects.create(**self.critic_1_data)

        critic_token = Token.objects.create(user=critic)

        self.client.credentials(HTTP_AUTHORIZATION="token " + critic_token.key)

        response1 = self.client.post(
            f"/api/movies/{movie.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        review_id = response1.data["id"]

        response2 = self.client.get(
            f"/api/movies/{movie.id}/reviews/{review_id}/",
        )

        self.assertEqual(response2.status_code, 200)

        self.assertIn("id", response2.data)
        self.assertIn("movie_id", response2.data)
        self.assertIn("critic", response2.data)

    def test_list_movie_reviews_200(self):
        genre = Genre.objects.create(**{"name": "anime"})

        movie = Movie.objects.create(**self.movie_data_no_genre_1)

        movie.genres.add(genre)

        response = self.client.get(f"/api/movies/{movie.id}/reviews/")

        self.assertEqual(response.status_code, 200)
