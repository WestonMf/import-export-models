import time
from paynow import Paynow
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book, Order
from django.contrib.auth.decorators import login_required


@login_required
def book_list(request):
    books = Book.objects.all()
    print(books)
    context = {
        "books": books
    }
    return render(request, "books/main.html", context)


def initiate_payment(request):
    # Paynow API details (replace with your actual Paynow API details)
    return_url = 'http://localhost/payment/callback'  # Replace with your callback URL

    # Initialize Paynow
    paynow = Paynow(settings.PAYNOW_INTEGRATION_ID,
                    settings.PAYNOW_INTEGRATION_KEY, return_url, return_url)

    # Create a payment
    payment = paynow.create_payment('Order #100', 'test@example.com')

    # Add items to the payment
    payment.add('Bananas', 2.50)
    payment.add('Apples', 3.40)

    # Send the payment to Paynow
    response = paynow.send(payment)

    if response.success:
        # Get the link to redirect the user to Paynow's payment page
        link = response.redirect_url

        # Get the poll URL (used to check the status of a transaction)
        poll_url = response.poll_url

        status = paynow.check_transaction_status(poll_url)
        time.sleep(300)
        print(f"status {status}")
        # Store the poll URL in your database or session for later use
        request.session['poll_url'] = poll_url

        # Redirect the user to Paynow's payment page
        return redirect(link)
    else:
        # Handle the case where payment initiation failed
        return HttpResponse("error")


def make_payment(request, id):
    book = get_object_or_404(Book, pk=id)
    paynow = Paynow(
        settings.PAYNOW_INTEGRATION_ID,
        settings.PAYNOW_INTEGRATION_KEY,
        'http://localhost:8000/books/return/',
        'http://localhost:8000/books/result/'
    )
    payment = paynow.create_payment(f'Order #{id}', 'test@example.com')
    # Passing in the name of the item and the price of the item
    payment.add('Bananas', 2.50)
    payment.add('Apples', 3.40)
    # Save the response from Paynow in a variable
    response = paynow.send(payment)
    print(response)
    if response.success:
        # Get the link to redirect the user to, then use it as you see fit
        link = response.redirect_url

        # Get the poll URL (used to check the status of a transaction). You might want to save this in your DB
        poll_url = response.poll_url
        print(f'Poll url {poll_url}')
        return redirect(link)
    else:
        return HttpResponse("The payment failed: " + response.error())
