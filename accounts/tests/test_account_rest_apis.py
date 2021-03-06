from django.core.urlresolvers import reverse
from rest_framework.test import (
    APITestCase,
)
from accounts.factories import UserFactory, CompanyFactory
from accounts.models import User
from StringIO import StringIO
from PIL import Image
from django.core.files.base import File


class AccountRestAPITestCase(APITestCase):

    def test_fetch_user_detail(self):
        user = UserFactory()
        self.client.force_login(user)
        url = reverse('api_accounts:current_user_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_key = [
            u'id',
            u'avatar',
            u'email',
            u'first_name',
            u'last_name',
            u'last_login',
            u'timezone'
        ]
        self.assertListEqual(sorted(response.json().keys()), sorted(expected_key))

    def test_change_account_profile(self):
        """
        Test change account
            first_name,
            last_name,
            timezone,
            uploading new avatar photo
        """
        image_obj = StringIO()
        image = Image.new("RGBA", size=(1,1,),)
        image.save(image_obj, 'JPEG')
        image_obj.seek(0)
        image_file = File(image_obj, name='test_ifle')

        user = UserFactory()
        self.client.force_login(user)
        url = reverse('api_accounts:current_user_detail')
        response = self.client.put(url, {
            'first_name': 'unique_first_name',
            'last_name': 'unique_last_name',
            'timezone': 'America/Los_Angeles',
            'avatar': image_file
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'unique_first_name')
        self.assertEqual(updated_user.last_name, 'unique_last_name')
        self.assertEqual(updated_user.timezone.zone, 'America/Los_Angeles')
        self.assertIsNotNone(updated_user.avatar)

    def test_change_account_password(self):
        user = UserFactory()
        old_password = 'test'
        new_password = 'new_password'
        user.set_password(old_password)
        user.save()
        self.client.force_login(user)
        url = reverse('api_accounts:current_user_detail')
        response = self.client.put(url, {
            'old_password': old_password,
            'new_password1': new_password,
            'new_password2': new_password,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(pk=user.pk)
        self.assertTrue(updated_user.check_password(new_password))

    def test_delete_account_avatar(self):
        image_obj = StringIO()
        image = Image.new("RGBA", size=(1, 1,), )
        image.save(image_obj, 'JPEG')
        image_obj.seek(0)
        image_file = File(image_obj, name='test_ifle')

        user = UserFactory()
        self.client.force_login(user)
        user.avatar = image_file
        user.save()
        url = reverse('api_accounts:current_user_detail')
        response = self.client.put(url, {
            'avatar': ''
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(pk=user.pk)
        self.assertTrue(bool(updated_user.avatar) is False)

    def test_change_account_password_failure_cases(self):
        # Should reject the password change request if old password is incorrect
        user = UserFactory()
        old_password = 'test'
        new_password = 'new_password'
        user.set_password(old_password)
        user.save()
        self.client.force_login(user)
        url = reverse('api_accounts:current_user_detail')

        # Test old password is incorrect
        response = self.client.put(url, {
            'old_password': 'wrong_password',
            'new_password1': new_password,
            'new_password2': new_password,
        }, format='json')

        self.assertEqual(response.status_code, 400)
        execpted = {
            u'old_password': [u'Old password is incorrect']
        }
        self.assertDictContainsSubset(execpted, response.json())

        # Test two passwords mismatch
        response = self.client.put(url, {
            'old_password': old_password,
            'new_password1': new_password,
            'new_password2': new_password + '1',
        }, format='json')

        self.assertEqual(response.status_code, 400)
        execpted = {
            u'new_password1': [u'Password1 and Password2 mismatch']
        }
        self.assertDictContainsSubset(execpted, response.json())

    def test_list_company_users(self):
        user1 = UserFactory()
        user2 = UserFactory()
        company = CompanyFactory()
        self.client.force_login(user1)

        user1.company = company
        user2.company = company
        user1.save()
        user2.save()

        response = self.client.get(reverse('api_accounts:company_users-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        first_user = response.json()[0]
        expected_keys = [
            'first_name',
            'last_name',
            'id',
            'email',
        ]

        self.assertItemsEqual(expected_keys, first_user.keys())
