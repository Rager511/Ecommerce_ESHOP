import json
import stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegistrationForm,LoginForm
from .models import Product, Commande, Category, Feedback
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import render


def index(request):
    categories = Category.objects.all()
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    category = request.GET.get('category')

    if category:
        product_object = Product.objects.filter(category__name__icontains=category)

    if item_name != '' and item_name is not None:
        product_object = product_object.filter(title__icontains=item_name)

    paginator = Paginator(product_object, 12)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)

    return render(request, 'index.html', {'product_object': product_object, 'categories': categories})


def product_by_category(request, category_name):
    categories = Category.objects.all()
    product_object = Product.objects.filter(category__name__icontains=category_name)

    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        product_object = product_object.filter(title__icontains=item_name)

    paginator = Paginator(product_object, 12)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)

    return render(request, 'product_by_category.html', {'product_object': product_object, 'categories': categories, 'category_name': category_name})


def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'detail.html', {'product': product_object})



def checkout(request):
    if request.method == 'POST':
        # Retrieve the form data
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        items = json.loads(request.POST.get('items'))
        total = request.POST.get('total')

        if not nom or not email or not address or not ville or not pays or not zipcode or not items or not total:
            return HttpResponse('Please fill out all the fields')

        # Save the Commande object
        com = Commande(items=items, total=total, nom=nom, email=email, address=address, ville=ville, pays=pays,
                       zipcode=zipcode)
        com.save()

        total_price = int(total[:-2])
        print(total_price)
        print(total_price * 100)

        # Redirect to the confirmation page
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Cart total',
                    },
                    'unit_amount': int(total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('confirmation')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('home')),
            metadata={
                'user_id': str(id),
                'last_name': nom,
                'email': email,
                'address': address,
                'zipcode': zipcode,
                'city': ville,
                'country': pays,
                'price': total_price
            }
        )
        return redirect(session.url)

    return render(request, 'checkout.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
        name=user.username,
    )
    return customer.id

@login_required
def payment(request):
    user=request.user
    if request.method == 'POST':
        try:
            # Retrieve the payment information from the form
            token = request.POST.get('stripeToken')
            amount = request.POST.get('amount')
            print(f"Amount: {amount}")  # Add this line to debug

            # Convert the amount from dollars to cents for Stripe
            if amount is not None:
                stripe_amount = int(float(amount) * 100)
            else:
                stripe_amount = 0

                # Create the charge on Stripe's servers
            charge = stripe.Charge.create(
                amount=stripe_amount,
                currency='usd',
                description='E-shop Payment',
                customer=create_stripe_customer(user),
            )

            # Display a success message to the user
            messages.success(request, 'Your payment was processed successfully!')
            return redirect('home')

        except stripe.error.CardError as e:
            # Display an error message to the user
            messages.error(request, f"There was an error processing your payment: {e.error.message}")
            return redirect('payment')

    else:
        # Render the payment form
        return render(request, 'payment.html')



def confirmation(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if rating and feedback:
            return redirect('home')

    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'confirmation.html', {'name': nom})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password!')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if rating and feedback:
            feedback_obj = Feedback(rating=rating, feedback=feedback)
            feedback_obj.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Please provide both a rating and feedback.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})
