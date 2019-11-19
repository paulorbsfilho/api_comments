from rest_framework.test import RequestsClient
from rest_framework.test import APIClient
from django.test import TestCase


class APITest(TestCase):

    def setUp(self):
        self.client = RequestsClient()

    def test_get_token(self):
        client = APIClient()
        response = client.post('/api-token-auth/', {'username': 'Bret', 'password': 'Bret123'}, format='json')
        print(response.status_code)
        assert response.status_code == 200

    def test_login_with_token(self):
        # headers={'Authorization': 'de37743763f5c4c62ad0b0fc7e7f945d05cfe14e'}
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    data={"username": "Bret", "password": "Bret123"})
        print(response)
        print(response.headers)
        print(response.status_code)
        assert response.status_code == 200

    def test_login_api_with_username(self):
        client = APIClient()
        client.login(username='Bret', password='Bret123')

    def test_api_root(self):
        response = self.client.get('http://localhost:8000')
        assert response.status_code == 200

    # def test_get_profiles(self):
    #     client = RequestsClient()
    #     response = client.get('http://localhost:8000/profiles/')
    #     assert response.status_code == 200

    def test_get_posts(self):
        response = self.client.get('http://localhost:8000/posts/')
        assert response.status_code == 200

    def test_get_post_comments(self):
        response = self.client.get('http://localhost:8000/post-comments/')
        assert response.status_code == 200

    def test_get_profile_posts(self):
        response = self.client.get('http://localhost:8000/profile-posts/')
        assert response.status_code == 200

    def test_get_profile_statistics(self):
        response = self.client.get('http://localhost:8000/users-statistics/')
        assert response.status_code == 200

    def test_post_post_owner(self):
        client = APIClient()
        client.post('/posts/', {'title': 'new idea', "body": "helooooooooo"}, format='json')
