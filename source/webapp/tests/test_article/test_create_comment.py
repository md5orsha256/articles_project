from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from webapp.models import Article


User = get_user_model()


class TestCreateComment(TestCase):
    def setUp(self) -> None:
        super(TestCreateComment, self).setUp()

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="TestUser",
            email="test@user.com",
        )
        cls.article = Article.objects.create(
            title="Test Article",
            content="Test Article Content",
            author=user
        )

    def test_success_create_comment(self):
        comment_author = User.objects.create(
            username="comment_author",
            email="comment_user@user.com",
        )

        comment = self.article.create_comment(
            author=comment_author,
            content="Test Comment Content"
        )

        self.assertTrue(self.article.comments.exists())
        self.assertEqual(self.article, comment.article)
        self.assertEqual(comment_author, comment.author)

    def test_unsuccessful_create_comment_with_author_does_not_exists(self):
        comment_author = User(
            username="comment_author",
            email="comment_user@user.com",
        )

        with self.assertRaises(ValidationError):
            self.article.create_comment(
                author=comment_author,
                content="1" * 2000
            )

        self.assertFalse(self.article.comments.exists())

    def test_unsuccessful_create_comment_content_gt_limit(self):
        comment_author = User.objects.create(
            username="comment_author",
            email="comment_user@user.com",
        )

        with self.assertRaises(ValidationError):
            comment = self.article.create_comment(
                author=comment_author,
                content="1" * 2001
            )

        self.assertFalse(self.article.comments.exists())
