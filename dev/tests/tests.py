from __future__ import print_function, absolute_import

from six import text_type

from django.test import TestCase as _TestCase, Client

from django.contrib.auth.models import User

from tests.models import TaggitExample


class TestCase(_TestCase):
    """Compatibility fix"""
    if not hasattr(_TestCase, 'assertRegex'):
        assertRegex = _TestCase.assertRegexpMatches
    if not hasattr(_TestCase, 'assertNotRegex'):
        assertNotRegex = _TestCase.assertNotRegexpMatches


class ModuleTest(TestCase):
    def setUp(self):
        """Sets the test environment"""
        self.user = User.objects.create(username='user', is_superuser=True, is_staff=True)
        self.user.set_password('password')
        self.user.save()

        self.taggit_examples = [
            TaggitExample.objects.create(name='example1', quantity=1, weight=1, price=1, kind='O'),
            TaggitExample.objects.create(name='example2', quantity=2, weight=2, price=2, kind='S'),
            TaggitExample.objects.create(name='example3', quantity=3, weight=3, price=3, kind='W'),
        ]

    def test_001_list_contains_action(self):
        """Whether the list view contains an action"""
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/admin/tests/taggitexample/')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(text_type(response.content), r'\<option\ value\=\"tag_wizard\"\>')

    def test_002_wizard_tagging(self):
        """Whether the wizard makes tagging properly"""
        c = Client()
        ids = [e.id for e in self.taggit_examples[1:]]
        c.login(username='user', password='password')
        response = c.post(
            '/admin/tests/taggitexample/',
            data={
                'action': 'tag_wizard',
                'select_across': 0,
                'index': 0,
                '_selected_action': ids
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/taggit/wizard/')
        response = c.get(response['location'])
        self.assertRegex(text_type(response.content), r'Bulk\ tagging\ 2\ Taggit\ Examples')
        response = c.post(
            '/taggit/wizard/',
            data={
                'taggit_bulk_wizard-current_step': 0,
                '0-tags': 'a, b',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/admin/tests/taggitexample/')
        response = c.get(response['location'])
        self.assertRegex(text_type(response.content), r'Tagged\ 2\ Taggit\ Examples')
        self.assertEqual(list(self.taggit_examples[0].tags.names()), [])
        self.assertEqual(list(self.taggit_examples[1].tags.names()), ['a', 'b'])
        self.assertEqual(list(self.taggit_examples[2].tags.names()), ['a', 'b'])

        ids = [e.id for e in self.taggit_examples[:-1]]
        response = c.post(
            '/admin/tests/taggitexample/',
            data={
                'action': 'tag_wizard',
                'select_across': 0,
                'index': 0,
                '_selected_action': ids
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/taggit/wizard/')
        response = c.get(response['location'])
        self.assertRegex(text_type(response.content), r'Bulk\ tagging\ 2\ Taggit\ Examples')
        response = c.post(
            '/taggit/wizard/',
            data={
                'taggit_bulk_wizard-current_step': 0,
                '0-tags': 'b, c',
                '0-clear': 'on',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/admin/tests/taggitexample/')
        response = c.get(response['location'])
        self.assertRegex(text_type(response.content), r'Untagged\ 2\ Taggit\ Examples')
        self.assertEqual(list(self.taggit_examples[0].tags.names()), [])
        self.assertEqual(list(self.taggit_examples[1].tags.names()), ['a'])
        self.assertEqual(list(self.taggit_examples[2].tags.names()), ['a', 'b'])
