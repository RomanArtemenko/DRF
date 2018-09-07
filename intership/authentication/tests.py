from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.


class SignUpTestCase(TestCase):

    def setUp(self):
        base_user = {
            'username': 'test1',
            'email': 'test1@mail.net',
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.valid_user = dict(base_user)
        self.invalid_user = dict(base_user)
        self.invalid_user.update({'confirm_password': 'swor'})

    def test_check_user_created(self):
        user_count_before = User.objects.count()
        res = self.client.post('/api/v1.0/auth/signup/', self.valid_user)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)

    def test_check_user_not_created(self):
        user_count_before = User.objects.count()
        res = self.client.post('/api/v1.0/auth/signup/', self.invalid_user)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)


class SignInTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        user = User.objects.create_user(username='test122',
            email='test1@mail.net',
            first_name='TestName',
            last_name='TestLastName',
            password='password'
                            )
        user.save()

    def setUp(self):
        base_user = {
            'username': 'test122',
            'password': 'password'
        }

        self.valid_user = dict(base_user)
        self.invalid_user = dict(base_user)
        self.invalid_user.update({'password': 'swodaadaaqqr'})

    def test_get_token_success(self):
        client_data = self.client
        res = client_data.post('/api/v1.0/auth/signin/', self.valid_user)
        self.assertIn('Token', res.content.decode('utf-8'))


    def test_get_token_fail(self):
        client_data = self.client
        res = client_data.post('/api/v1.0/auth/signin/', self.invalid_user)
        self.assertIn('Wrong password', res.content.decode('utf-8'))

