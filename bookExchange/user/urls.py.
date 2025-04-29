from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URLs для анонімних користувачів
    path('', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='book_exchange/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    # URLs для аутентифікованих користувачів
    path('my-books/', views.my_books, name='my_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/offer/', views.make_offer, name='make_offer'),
    path('my-offers/', views.my_offers, name='my_offers'),
    path('offers/<int:offer_id>/<str:action>/', views.respond_to_offer, name='respond_to_offer'),
]
