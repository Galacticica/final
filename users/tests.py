"""
File: tests.py
Author: Reagan Zierke
Date: 2025-05-06
Description: Unit tests for the Users app.
This file contains tests for the views_user.py file. These cover the user profile, and leveling up functionality.
"""



from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "discord_id": "12345",
            "username": "TestUser",
        }
        self.existing_user = CustomUser.objects.create(
            discord_id="67890", username="ExistingUser", level=1, xp=10, money=100
        )

    def test_get_profile_create_user(self):
        '''
        Test creating a new user via the GetProfileView.
        '''
        response = self.client.post('/users/profile/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['discord_id'], self.user_data['discord_id'])
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_get_profile_update_user(self):
        '''
        Test updating an existing user's username via the GetProfileView.
        '''
        update_data = {"discord_id": self.existing_user.discord_id, "username": "UpdatedUser"}
        response = self.client.post('/users/profile/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.username, "UpdatedUser")

    def test_get_profile_missing_discord_id(self):
        '''
        Test error response when discord_id is missing in GetProfileView.
        '''
        response = self.client.post('/users/profile/', {"username": "NoDiscordID"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_level_up_success(self):
        '''
        Test leveling up a user with sufficient XP via the LevelUpView.
        '''
        self.existing_user.xp = self.existing_user.xp_needed
        self.existing_user.save()
        response = self.client.post('/users/level_up/', {"discord_id": self.existing_user.discord_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.level, 2)
        self.assertEqual(self.existing_user.xp, 0)

    def test_level_up_insufficient_xp(self):
        '''
        Test error response when user has insufficient XP in LevelUpView.
        '''
        response = self.client.post('/users/level_up/', {"discord_id": self.existing_user.discord_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_level_up_missing_discord_id(self):
        '''
        Test error response when discord_id is missing in LevelUpView.
        '''
        response = self.client.post('/users/level_up/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

