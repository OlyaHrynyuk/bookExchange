from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Category, Book, Offer

app_label = 'user'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'owner', 'category', 'available', 'created_at')
    list_filter = ('available', 'category', 'created_at')
    search_fields = ('title', 'author', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'offered_book', 'requested_book', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    actions = ['reset_password']

    def reset_password(self, request, queryset):
        for user in queryset:
            user.set_password('password123')
            user.save()
        self.message_user(request, f"Пароль змінено для {queryset.count()} користувачів.")

    reset_password.short_description = "Змінити паролі для вибраних користувачів"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)