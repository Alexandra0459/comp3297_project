import csv, datetime
from ASP.models import ClinicManager, MedicineSupply, Order, Dispatcher, Location
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate
from .forms import SignupForm,RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/asp/clinicmanager/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/asp/admin/')
    else:
        return render_to_response('login.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        form1 = RegisterForm(request.POST)
        if form1.is_valid():
            user = form1.save(commit=False)
            user.is_active = False
            user.save()
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class CMViewsSupply(ListView):
    model = MedicineSupply
    clinic_manager = ClinicManager.objects.get(pk=1) # change after login designed

    def construct_order(request):
        items = ''
        weight = 0.0
        for i in range(1, 10):
            amount = request.POST.get('amount' + str(i))
            if amount is None:
                break
            if amount != '':
                priority = request.POST.get('priority')
                amount = int(amount)
                id = request.POST.get('id' + str(i))
                name = request.POST.get('name' + str(i))
                weight += float(request.POST.get('weight' + str(i))) * amount
                items += "id: %s; name: %s; amount: %s.\n" %(id, name, amount)
        if items != '':
            CMViewsSupply.add_order(CMViewsSupply, items, weight, priority)

        return redirect('clinic-manager')

    def add_order(self, items, weight, priority):
        order = Order()

        order.clinic_manager = self.clinic_manager
        order.location = self.clinic_manager.location
        order.items = items
        order.weight = weight
        order.priority = priority
        order.timeQP = datetime.datetime.now()

        order.save()

        return

class DPViewsOrder(ListView):
    order_list = []
    total_weight = 0
    max_weight = 25

    def get_queryset(self):
        return Order.objects.filter(status__exact='QD').order_by('-priority')

    def update_order(request):
        order_id = request.POST.get('order')
        order = Order.objects.get(id=order_id)


        if DPViewsOrder.total_weight + order.weight > DPViewsOrder.max_weight:
            return redirect('dispatcher')

        DPViewsOrder.total_weight += order.weight
        order.status = 'DI'
        order.timeDI = datetime.datetime.now()
        order.save()
        DPViewsOrder.order_list.append(order)
        return redirect('dispatcher')

    def get_csv(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=dispacher_order.csv'
        writer = csv.writer(response)

        writer.writerow(['Start from Queen Mary Hospital'])

        for order in DPViewsOrder.order_list:
            location = order.location
            location_obj = Location.objects.get(name=location)
            latitude = location_obj.latitude
            longtitude = location_obj.longitude
            altitude = location_obj.altitude

            writer.writerow([f'{location}: {latitude}-{longtitude}-{altitude}'])

        DPViewsOrder.order_list.clear()
        DPViewsOrder.total_weight = 0
        return response

