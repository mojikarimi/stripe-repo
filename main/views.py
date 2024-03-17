from django.conf import settings
from django.shortcuts import render, redirect
import stripe
from django.contrib import messages
# Create your views here.
from django.urls import reverse

stripe.api_key = 'sk_test_51OF9shIKF4RrMLl2nKHUoez72hzKFsQd1Lf9pOp2TYjM99oeCupk1rBhtRfVJiUVJZqCjmitHRik9ZKHvjNr2AWa00KAVeR3zR'


def index(request):
    # for main page
    if request.method == 'POST':
        amount = request.POST.get('amount')
        request.session['amount'] = int(amount) * 100
        return redirect('payment')
    return render(request, "index.html")


def payment(request):
    # This view is bought for the final registration and the information is stored in the strip
    key = settings.STRIPE_PUBLIC_KEY
    amount = request.session['amount']
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=int(request.POST.get('amount')),
            currency='usd',
            description='Payment for your product or service',
            source=request.POST.get('stripeToken'),
        )
        if charge['status'] == 'succeeded':
            messages.success(request, 'Payment successful!')
            return redirect('success')
        elif charge['status'] == 'failed':
            messages.error(request, 'my message')
            return redirect('cancel')
        else:
            messages.warning(request, 'my message')
            return redirect('index')

    return render(request, "my_view.html", {'key': key, 'amount': amount})


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
