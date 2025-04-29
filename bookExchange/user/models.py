from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує розгляду'),
        ('accepted', 'Прийнято'),
        ('rejected', 'Відхилено'),
    ]

    offered_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offers_made')
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offers_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Пропозиція: {self.offered_book.title} за {self.requested_book.title}"