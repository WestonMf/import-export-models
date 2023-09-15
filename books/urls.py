from django.urls import path
from .views import book_list, make_payment, initiate_payment
app_name = "books"
urlpatterns = [
    path("", book_list, name="books"),
    path("payment/", initiate_payment, name="initiate_payment"),
    path('<int:id>/payment', make_payment, name="make_payment"),
]
