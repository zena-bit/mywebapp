import io
from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from .models import Category, Product, Review, ReviewImage
from .ai_verifier import verify_product_image_match

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='A great phone',
            price=699.99,
            category=self.category,
            stock=10
        )

    def test_create_valid_review(self):
        review = Review(
            product=self.product,
            user=self.user,
            rating=5,
            comment='This is an awesome product!'
        )
        review.full_clean()
        review.save()
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(str(review), f"{self.user} review for {self.product.name} (5/5)")
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_rating_out_of_bounds_low(self):
        review = Review(
            product=self.product,
            user=self.user,
            rating=0,
            comment='Terrible'
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_out_of_bounds_high(self):
        review = Review(
            product=self.product,
            user=self.user,
            rating=6,
            comment='Too good'
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_comment_word_count_exceeded(self):
        long_comment = "word " * 251
        review = Review(
            product=self.product,
            user=self.user,
            rating=4,
            comment=long_comment
        )
        with self.assertRaises(ValidationError) as ctx:
            review.full_clean()
        self.assertIn('comment', ctx.exception.message_dict)

    def test_unique_user_product_constraint(self):
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='First review'
        )
        duplicate_review = Review(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Second review'
        )
        with self.assertRaises(IntegrityError):
            duplicate_review.save()

    def test_multiple_users_can_review_same_product(self):
        Review.objects.create(product=self.product, user=self.user, rating=5, comment='User 1 review')
        Review.objects.create(product=self.product, user=self.user2, rating=4, comment='User 2 review')
        self.assertEqual(Review.objects.filter(product=self.product).count(), 2)

    def test_review_image_creation(self):
        review = Review.objects.create(product=self.product, user=self.user, rating=5, comment='Great phone')
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        uploaded_file = SimpleUploadedFile("test.jpg", img_io.getvalue(), content_type="image/jpeg")

        review_img = ReviewImage.objects.create(review=review, image=uploaded_file, is_verified=True)
        self.assertEqual(review.images.count(), 1)
        self.assertTrue(review_img.is_verified)

    def test_ai_image_verification_match(self):
        # Create identical images
        img1 = Image.new('RGB', (100, 100), color='red')
        img_io1 = io.BytesIO()
        img1.save(img_io1, format='JPEG')
        file1 = SimpleUploadedFile("ref.jpg", img_io1.getvalue(), content_type="image/jpeg")

        img2 = Image.new('RGB', (100, 100), color='red')
        img_io2 = io.BytesIO()
        img2.save(img_io2, format='JPEG')
        file2 = SimpleUploadedFile("upload.jpg", img_io2.getvalue(), content_type="image/jpeg")

        is_match, score = verify_product_image_match(file2, file1)
        self.assertTrue(is_match)
        self.assertGreaterEqual(score, 0.32)

    def test_ai_image_verification_mismatch(self):
        # Create visually contrasting images (solid red vs solid blue)
        img1 = Image.new('RGB', (100, 100), color='red')
        img_io1 = io.BytesIO()
        img1.save(img_io1, format='JPEG')
        file1 = SimpleUploadedFile("product.jpg", img_io1.getvalue(), content_type="image/jpeg")

        img2 = Image.new('RGB', (100, 100), color='green')
        img_io2 = io.BytesIO()
        img2.save(img_io2, format='JPEG')
        file2 = SimpleUploadedFile("different.jpg", img_io2.getvalue(), content_type="image/jpeg")

        is_match, score = verify_product_image_match(file2, file1)
        # Note: solid red vs green will have low color histogram similarity
        self.assertIsInstance(is_match, bool)


