from dataclasses import fields
from django.test import TestCase
from movies.models import Genre, Movie, Review
from users.models import User
from django.db.models import fields
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class TestUserModelSerializer(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_has_expected_fields(self):

        """
        Testa se a model possui os atributos corretos
        """

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

    def test_has_correct_lenght_constraints(self):
        """
        Testa se a model possui as constraints corretas
        """

        fields_to_check_length_constraints = [
            "email",
            "username",
            "first_name",
            "last_name",
        ]

        fields_to_check_nullability_constraints = [
            "email",
            "username",
            "first_name",
            "last_name",
            "birthdate",
            "bio",
            "is_critic",
        ]

        expected_values_to_max_length_constraint = [127, 20, 50, 50]
        expected_values_to_nulability_constraint = [
            False,
            False,
            False,
            False,
            False,
            True,
            False,
        ]
        for index, fieldname in enumerate(fields_to_check_length_constraints):
            self.assertEqual(
                User._meta.get_field(fieldname).max_length,
                expected_values_to_max_length_constraint[index],
            )

        for index, fieldname in enumerate(fields_to_check_nullability_constraints):
            self.assertEqual(
                User._meta.get_field(fieldname).null,
                expected_values_to_nulability_constraint[index],
                {
                    "message": f"{fieldname} deve ser null={expected_values_to_nulability_constraint[index]}"
                },
            )

        self.assertEqual(
            User._meta.get_field("bio").default,
            None,
            {"message": "Bio default deve ser none"},
        )
        self.assertEqual(
            User._meta.get_field("is_critic").default,
            False,
            {"message": "Is_critic default deve ser false"},
        )


class TestUserMovieReviewViews(APITestCase):
    @classmethod
    def setUpTestData(cls):

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
            "is_staff": True,
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

        cls.user_invalid_types = {
            "email": 123,
            "username": 123,
            "password": 123,
            "first_name": 123,
            "last_name": 123,
            "birthdate": 123,
            "bio": 123,
            "is_critic": 123,
        }

        cls.required_keys = {
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "birthdate",
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

        cls.review_wrong_recomendation = {
            "stars": 10,
            "review": "not very nice soup",
            "spoilers": False,
            "recomendation": "Comment random",
        }

        cls.USERS_POST_URL = "/api/users/register/"
        cls.URL_LOGIN = "/api/users/login/"
        cls.USERS_BASE_URL = "/api/users/"
        cls.MOVIE_BASE_URL = "/api/movies/"

        cls.user = User.objects.create(**cls.regular_user_data)
        cls.user_token = Token.objects.create(user=cls.user)
        cls.critic_1 = User.objects.create_user(**cls.critic_1_data)
        cls.critic_1_token = Token.objects.create(user=cls.critic_1)
        cls.admin_user = User.objects.create(**cls.admin_data)
        cls.admin_user_token = Token.objects.create(user=cls.admin_user)

        cls.genre = Genre.objects.create(**{"name": "anime"})
        cls.movie1 = Movie.objects.create(**cls.movie_data_no_genre_1)
        cls.movie2 = Movie.objects.create(**cls.movie_data_no_genre_2)
        cls.movie1.genres.add(cls.genre)
        cls.movie2.genres.add(cls.genre)

    def test_create_user_201(self):

        """
        Testa criação de usuário
        """

        response = self.client.post(
            self.USERS_POST_URL, self.regular_user_data_2, format="json"
        )

        self.assertEquals(201, response.status_code)
        self.assertIn("updated_at", response.json())
        self.assertIn("id", response.json())

    def test_create_user_duplicate_400(self):
        """
        Testa criação de usuário duplicado
        """

        self.user = User.objects.create(**self.regular_user_data_2)

        response = self.client.post(
            self.USERS_POST_URL, self.duplicate_user_data, format="json"
        )

        self.assertEquals(400, response.status_code)
        self.assertIn("username already exists", response.data["username"])
        self.assertIn("email already exists", response.data["email"])

    def test_create_user_without_keys_400(self):
        """
        Testa criação de usuário vazio
        """

        response = self.client.post(self.USERS_POST_URL, {}, format="json")

        self.assertEquals(400, response.status_code)

        for key in self.required_keys:
            self.assertIn("This field is required.", response.data[key])

    def test_create_user_invalid_key_type(self):
        """
        Testa criação de usuário com chaves inválidas
        """

        response = self.client.post(
            self.USERS_POST_URL, self.user_invalid_types, format="json"
        )

        self.assertEquals(400, response.status_code)

    def test_login_critic(self):
        """
        Testa login de critico
        """

        response = self.client.post(self.URL_LOGIN, self.critic_1_login)

        self.assertEqual(self.critic_1.auth_token.key, response.data["token"])

    def test_owner_list_user_200(self):
        """
        Testa listagem do próprio usuário
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}{self.critic_1.id}/")

        self.assertEqual(response.status_code, 200)

    def test_non_owner_list_user_403(self):
        """
        Testa listagem de outro usuário
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}{self.critic_1.id}/")

        self.assertEqual(response.status_code, 403)

    def test_list_user_token_null_401(self):
        """
        Testa listagem sem token
        """

        response = self.client.get(f"{self.USERS_BASE_URL}{self.critic_1.id}/")

        self.assertEqual(response.status_code, 401)

    def test_list_user_admin_token_200(self):
        """
        Testa listagem como admin
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}{self.critic_1.id}/")

        self.assertEqual(response.status_code, 200)

    def test_list_users_admin_200(self):
        """
        Testa listagem geral como admin
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}")

        self.assertEqual(response.status_code, 200)

    def test_list_users_admin_pagination_200(self):
        """
        Testa paginação de listagem geral
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}")

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            "results",
            response.data,
            {"message": "Deve haver uma chave results na resposta"},
        )

    def test_list_users_regular_user_403(self):
        """
        Testa listagem geral como usuario normal
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}")

        self.assertEqual(response.status_code, 403)

    def test_list_users_critic_403(self):
        """
        Testa listagem geral como crítico
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.get(f"{self.USERS_BASE_URL}")

        self.assertEqual(response.status_code, 403)

    # ##### Movies #####

    def test_created_movie_has_expected_fields_201(self):
        """
        Testa criação de filmes como admin
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}", self.movie_data_1, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("genres", response.data)
        self.assertIn("id", response.data["genres"][0])

    def test_create_movie_regular_user_403(self):
        """
        Testa criação de filmes como usuário regular
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}", self.movie_data_1, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_create_movie_critic_user_403(self):
        """
        Testa criação de filmes como crítico
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}", self.movie_data_1, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_create_movie_null_token_401(self):
        """
        Testa criação de filmes sem token
        """

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}", self.movie_data_1, format="json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_list_movies_200(self):
        """
        Testa listagem de filmes
        """

        response = self.client.get(f"{self.MOVIE_BASE_URL}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["count"], 2, {"message": "Deve haver o count de paginação"}
        )
        self.assertIn(
            "title",
            response.data["results"][0],
            {"message": "Deve haver uma chave title"},
        )
        self.assertIn(
            "id",
            response.data["results"][0]["genres"][0],
            {"message": "Deve haver uma chave id"},
        )

    def test_list_specific_movie_200(self):
        """
        Testa listagem de um filme
        """

        response = self.client.get(f"{self.MOVIE_BASE_URL}{self.movie1.id}/")

        self.assertEqual(response.status_code, 200)

    def test_list_movie_unexintent_404(self):
        """
        Testa listagem de um filme inexistente
        """

        response = self.client.get(f"{self.MOVIE_BASE_URL}1000/")

        self.assertEqual(response.status_code, 404)

    def test_delete_movie_admin_204(self):
        """
        Testa deleção de um filme como admin
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.delete(f"{self.MOVIE_BASE_URL}{self.movie1.id}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_movie_regular_user_403(self):
        """
        Testa deleção de um filme como usuário regular
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.delete(f"{self.MOVIE_BASE_URL}{self.movie1.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
            {"message": "Deve haver uma mensagem de permissão"},
        )

    def test_delete_movie_critic_403(self):
        """
        Testa deleção de um filme como crítico
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.delete(f"{self.MOVIE_BASE_URL}{self.movie1.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
            {"message": "Deve haver uma mensagem de permissão"},
        )

    def test_delete_movie_null_token_401(self):
        """
        Testa deleção de um filme sem tokens
        """

        response = self.client.delete(f"{self.MOVIE_BASE_URL}{self.movie1.id}/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
            {"message": "Deve haver uma mensagem de permissão"},
        )

    def test_update_movie_superuser_200(self):
        """
        Testa atualização de um filme como admin
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.admin_user_token.key)

        response = self.client.patch(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/", self.movie_data_2, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            self.movie_data_2["title"],
            {"message": "O filme deve ser atualizado corretamente"},
        )

    def test_update_movie_regular_user_403(self):
        """
        Testa atualização de um filme como usuário normal
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.patch(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/", self.movie_data_2, format="json"
        )

        self.assertEqual(response.status_code, 403)

    # ###### Reviews ######

    def test_create_review_critic_201(self):
        """
        Testa criação de review como crítico
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        expected_returned_keys = {
            "id",
            "movie_id",
            "critic",
            "recomendation",
            "stars",
            "spoilers",
            "review",
        }
        result_returned_keys = set(response.json().keys())

        self.assertSetEqual(
            expected_returned_keys,
            result_returned_keys,
            {"message": "Deve conter as chaves esperadas"},
        )

    def test_create_review_regular_user_403(self):
        """
        Testa criação de review como usuário normal
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.user_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_create_duplicate_review_401(self):
        """
        Testa criação duplicada de review
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response1 = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        response2 = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        self.assertEqual(response2.status_code, 401)

    def test_create_review_invalid_start_400(self):
        """
        Testa criação de review com estrelas invalidas
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_too_many_stars,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this value is less than or equal to 10.",
            response.data["stars"],
            {"message": "Deve haver uma mensagem de erro"},
        )

    def test_create_review_invalid_recomendation_400(self):
        """
        Testa criação de review com recomendação inválida
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_wrong_recomendation,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            '"Comment random" is not a valid choice.',
            response.data["recomendation"],
            {"message": "Deve haver uma mensagem de erro"},
        )

    def test_list_specific_review_critic_owner_200(self):
        """
        Testa listagem de review do próprio crítico
        """

        self.client.credentials(HTTP_AUTHORIZATION="token " + self.critic_1_token.key)

        response1 = self.client.post(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/",
            self.review_1_movie_1,
            format="json",
        )

        review_id = response1.data["id"]

        response2 = self.client.get(
            f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/{review_id}/",
        )

        self.assertEqual(response2.status_code, 200)

        expected_returned_keys = {
            "id",
            "movie_id",
            "critic",
            "recomendation",
            "stars",
            "spoilers",
            "review",
        }
        result_returned_keys = set(response2.json().keys())

        self.assertSetEqual(
            expected_returned_keys,
            result_returned_keys,
            {"message": "Deve conter as chaves esperadas"},
        )

    def test_list_movie_reviews_200(self):
        """
        Testa listagem geral de reviews
        """
        response = self.client.get(f"{self.MOVIE_BASE_URL}{self.movie1.id}/reviews/")

        self.assertEqual(response.status_code, 200)
