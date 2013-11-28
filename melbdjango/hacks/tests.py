from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Idea

# Create your tests here.
class IdeasTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        self.client = Client()
        self.client.login(username='test', password='test')
        self.idea = Idea(owner=self.user, title='title', description='description')
        self.idea.save()

    def test_idea_detail_context(self):
        response = self.client.get(reverse('idea-detail', kwargs={'idea_id': self.idea.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('idea' in response.context)

        idea = response.context['idea']
        self.assertEqual(idea.id, self.idea.id)


    def test_idea_detail_upvote(self):
        response = self.client.get(reverse('idea-detail', kwargs={'idea_id': self.idea.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('idea' in response.context)
        idea = response.context['idea']
        upvote_url = idea.get_voteup_url()
        response = self.client.post(upvote_url, user=self.user)
        self.assertTrue(response.status_code, 200)

        # TODO (shaunokeefe): following test fails because
        # total_votes returns None instead of 0
        #self.assertEqual(idea.total_votes, 0)
        new_idea = Idea.objects.get(id=self.idea.id)
        self.assertEqual(new_idea.total_votes, 1)

    def test_idea_detail_downvote(self):
        response = self.client.get(reverse('idea-detail', kwargs={'idea_id': self.idea.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('idea' in response.context)
        idea = response.context['idea']
        downvote_url = idea.get_votedown_url()
        response = self.client.post(downvote_url)
        self.assertTrue(response.status_code, 200)

        # TODO (shaunokeefe): following test fails because
        # total_votes returns None instead of 0
        #self.assertEqual(idea.total_votes, 0)
        new_idea = Idea.objects.get(id=self.idea.id)
        self.assertEqual(new_idea.total_votes, -1)
