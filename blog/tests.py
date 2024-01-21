from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment
from blog.templatetags import blog_extras
import datetime
from django.utils.html import format_html
from blog.views import post_detail
from loguru import logger

class AuthorDetailsFilterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpassword"
        )
        self.post_author = User.objects.create_user(
            username="postauthor",
            password="postpassword"
        )
        self.post = Post.objects.create(
        created_at=datetime.datetime.now(),
        title="Test Post",
        slug="test-post",
        content="Blah blah blah",
        author=self.post_author,
        status="P"
        )

    def test_author_details_with_current_user(self):
        # Test when the current user is the post author
        logged_in = self.client.login(
            username=self.user.username,
            password="testpassword"
        )
        response = self.client.get(reverse("blog-index"))
        self.assertTrue(logged_in)
        self.assertEqual(
            blog_extras.author_details(self.post_author, self.post_author),
            format_html("<strong>Me!</strong>")
        )

    def test_author_details_without_current_user(self):
        # Test when the current user is not the post author
        response = self.client.get(reverse("post-detail", kwargs={'slug':self.post.slug}))
        self.assertEqual(
            blog_extras.author_details(self.post_author, None),
            format_html(" ")
        )

    def test_author_details_no_user_data(self):
        # Test when the user data is not found in the database
        User.objects.filter(pk=self.post_author.id).delete()
        response = self.client.get(reverse("post-detail", kwargs={'slug':self.post.slug}))
        self.assertEqual(
            blog_extras.author_details(self.post_author, None),
            " "
        )
        
