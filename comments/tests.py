from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import RequestsClient
from rest_framework.test import APIClient
from django.test import TestCase, Client


class APITest(TestCase):

    # def setUp(self):
    #     self.client = APIClient()

    def test_login_with_token(self):
        client = RequestsClient()
        response = client.post('http://localhost:8000/api-token-auth/', {'username':'Bret','password':'Bret123'})
        print(response.json())
        # client = APIClient()
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_login_api_with_username(self):
        client = APIClient()
        client.login(username='Bret', password='Bret123')

    def test_api_root(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000')
        assert response.status_code == 200

    # def test_get_profiles(self):
    #     client = RequestsClient()
    #     response = client.get('http://localhost:8000/profiles/')
    #     assert response.status_code == 200

    def test_get_posts(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000/posts/')
        assert response.status_code == 200

    def test_get_post_comments(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000/post-comments/')
        assert response.status_code == 200

    def test_get_profile_posts(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000/profile-posts/')
        assert response.status_code == 200

    def test_get_profile_statistics(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000/users-statistics/')
        assert response.status_code == 200

    def test_post_post_owner(self):
        client = APIClient()
        client.post('/posts/', {'title': 'new idea', "body": "helooooooooo"}, format='json')
