import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestChatbotAPI:

    def test_create_chat_message(self):
        client = APIClient()
        url = reverse('chat:create')

        # Test case: Create a chat message successfully
        payload = {'message': 'Hello, Chatbot!'}
        response = client.post(url, data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == payload['message']
        assert 'id' in response.data

        # Test case: Create a chat message without message field (should fail)
        payload = {}
        response = client.post(url, data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_chat_message(self):
        client = APIClient()
        url = reverse('chat:list')

        # Test case: Get a list of chat messages (should be empty initially)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

        # Create a chat message
        payload = {'message': 'Hello, Chatbot!'}
        client.post(reverse('chat:create'), data=payload)

        # Test case: Get a list of chat messages (should have one message)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['message'] == payload['message']

    def test_delete_chat_message(self):
        client = APIClient()
        url = reverse('chat:list')

        # Create a chat message
        payload = {'message': 'Hello, Chatbot!'}
        response = client.post(reverse('chat:create'), data=payload)
        chat_id = response.data['id']

        # Test case: Delete a chat message (should succeed)
        delete_url = reverse('chat:detail', kwargs={'pk': chat_id})
        response = client.delete(delete_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Test case: Delete a non-existent chat message (should fail)
        response = client.delete(delete_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

