from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Book, Offer, Category
from .forms import RegistrationForm, BookForm, OfferForm


# Анонімні користувачі
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('book_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def book_list(request):
    books = Book.objects.filter(available=True)
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)

    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_id
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    offer_form = None

    if request.user.is_authenticated and book.owner != request.user:
        offer_form = OfferForm(user=request.user)

    context = {
        'book': book,
        'offer_form': offer_form
    }
    return render(request, 'book_detail.html', context)


# Аутентифіковані користувачі
@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user)
    return render(request, 'my_books.html', {'books': books})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Книгу додано успішно!')
            return redirect('my_books')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form, 'action': 'Додати'})


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книгу оновлено успішно!')
            return redirect('my_books')
    else:
        form = BookForm(instance=book)

    return render(request, 'book_form.html', {'form': form, 'action': 'Редагувати'})


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книгу видалено успішно!')
        return redirect('my_books')

    return render(request, 'book_confirm_delete.html', {'book': book})


@login_required
def make_offer(request, book_id):
    requested_book = get_object_or_404(Book, id=book_id)

    # Перевірка, що користувач не намагається обміняти свою ж книгу
    if requested_book.owner == request.user:
        messages.error(request, 'Ви не можете запропонувати обмін на власну книгу!')
        return redirect('book_detail', book_id=book_id)

    if request.method == 'POST':
        form = OfferForm(request.user, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.requested_book = requested_book

            # Перевірка на наявність дублікатів пропозицій
            existing_offer = Offer.objects.filter(
                offered_book=offer.offered_book,
                requested_book=requested_book,
                status='pending'
            ).exists()

            if existing_offer:
                messages.error(request, 'Ви вже зробили пропозицію обміну для цієї книги!')
            else:
                offer.save()
                messages.success(request, 'Пропозицію обміну створено успішно!')

            return redirect('book_detail', book_id=book_id)
    else:
        form = OfferForm(user=request.user)

    return render(request, 'make_offer.html', {
        'form': form,
        'requested_book': requested_book
    })


@login_required
def my_offers(request):
    # Пропозиції, які зробив користувач
    outgoing_offers = Offer.objects.filter(offered_book__owner=request.user)

    # Пропозиції, які отримав користувач
    incoming_offers = Offer.objects.filter(requested_book__owner=request.user)

    context = {
        'outgoing_offers': outgoing_offers,
        'incoming_offers': incoming_offers
    }
    return render(request, 'my_offers.html', context)


@login_required
def respond_to_offer(request, offer_id, action):
    offer = get_object_or_404(Offer, id=offer_id, requested_book__owner=request.user)

    if action == 'accept':
        offer.status = 'accepted'
        # Позначити обидві книги як недоступні
        offer.offered_book.available = False
        offer.requested_book.available = False
        offer.offered_book.save()
        offer.requested_book.save()
        messages.success(request, 'Пропозицію обміну прийнято!')
    elif action == 'reject':
        offer.status = 'rejected'
        messages.success(request, 'Пропозицію обміну відхилено!')

    offer.save()
    return redirect('my_offers')