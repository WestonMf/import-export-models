from typing import List, Optional
from django_unicorn.components import UnicornView, QuerySetType
from django.contrib.auth.models import User
from books.models import Order
from django.db.models import F


class CartView(UnicornView):
    user_books: QuerySetType[Order] = None
    user_pk: int
    total: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.user_pk = kwargs.get("user")
        self.user_books = Order.objects.filter(customer=self.user_pk)
        self.get_total()

    def add_book(self, book_id):
        book, created = Order.objects.get_or_create(
            customer_id=self.user_pk, book_id=book_id)
        if not created:
            book.quantity = F('quantity') + 1
            book.save()
        self.user_books = Order.objects.filter(customer=self.user_pk)
        self.get_total()

    def get_total(self):
        self.total = sum(
            order.total_price for order in self.user_books
        )

    def delete_book(self, book_id):
        book = Order.objects.get(pk=book_id)
        book.delete()
        self.user_books = self.user_books.exclude(pk=book_id)
        self.get_total()
