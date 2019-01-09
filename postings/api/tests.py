from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth import get_user_model
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse

# Automated
# blank db

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User.objects.create(username='testuser', email='test@test.com')
        user_obj.set_password('somerandompassword')
        user_obj.save()
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='New Title', 
            content='some_random_content'
            )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
    
    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        # tested get list item
        data = {}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_post_item(self):
        # tested get list item
        data = {"title":"some random title", "content":"some random content"}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        # tested get list item
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        #url = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        # tested get list item
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title":"some random title", "content":"some random content"}
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        # tested get list item
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title":"some random title", "content":"some more content"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) #JWT <token>
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_item_with_user(self):
        # tested get list item
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {"title":"some random title", "content":"some random content"}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        # tested get list item
        owner = User.objects.create(username='testuser222')
        blog_post = BlogPost.objects.create(
            user=owner,
            title='New Title', 
            content='some_random_content'
            )

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        url = blog_post.get_api_url()
        data = {"title":"some random title", "content":"some more content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_login(self):
        data = {
            'username': 'testuser',
            'password': 'somerandompassword'
        }
        url = api_reverse('api-login')
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            url = blog_post.get_api_url()
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token) #JWT <token>
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)