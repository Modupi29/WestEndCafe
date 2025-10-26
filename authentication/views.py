# Django imports for views and helpers
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomeUser, Profile
from menu.models import MenuItem
# =============================
# Home Page View
# =============================
def home_view(request):
    # Retrieve any stored messages to display in the template (success/errors)
    messages_to_display = messages.get_messages(request)
    return render(request, 'registration/base.html', {
        'messages': messages_to_display,
    })

# =============================
# User Registration View
# =============================
def user_registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save user object but don't activate yet
            user = form.save(commit=False)
            user.is_active = False

            # Prepare account activation email
            current_site = get_current_site(request)
            protocol = request.scheme  # Detect 'http' or 'https'
            email_subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])

            try:
                email.send()
                user.save()
                messages.success(request, 'Please check your email to complete the registration.')
                return redirect('home')
            except Exception as e:
                # Fallback if email fails
                messages.error(request, f'Email could not be sent: {e}')
                return render(request, 'registration/sign_up.html', {'form': form})
        else:
            messages.error(request, 'Invalid form sent.')
            return render(request, 'registration/sign_up.html', {'form': form})
    else:
        # GET request — present blank sign-up form
        form = RegistrationForm()
        return render(request, 'registration/sign_up.html', {'form': form})

# =============================
# Account Activation View
# =============================
def account_activation_view(request, uidb64, token):
    try:
        # Decode the UID from the activation URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomeUser.objects.get(pk=uid)
    except (CustomeUser.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    # Validate token and activate account
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)  # Log the user in after activation
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Your activation link is invalid or expired.')
        return redirect('home')

# =============================
# Login View
# =============================
def login_view(request):
    messages_to_display = messages.get_messages(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get credentials from form
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active and user.user_type == 'Customer':
                login(request, user)
                return redirect('dashboard')
            elif user is not None and user.user_type == 'Admin':
                login(request, user)
                return redirect('admin-dashboard')
            else:
                messages.error(request, "Invalid credentials.")
                return render(request, "registration/login.html", {'form': form})
        else:
            messages.error(request, "Failed to login.")
            return render(request, "registration/login.html", {'form': form})
    else:
        # GET request — display the login form
        form = LoginForm()
        return render(request, "registration/login.html", {'form': form})

# =============================
# Logout View
# =============================
@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')

# =============================
# Index View (Protected)
# =============================
@login_required()
def index_view(request):
    special_menu_items = MenuItem.objects.filter(category = 'SPECIAL', available=True)
    breakfast_menu_items = MenuItem.objects.filter(category='BREAKFAST', available=True)
    main_course_menu_items = MenuItem.objects.filter(category='MAIN MEALS', available=True)
    soft_drink_menu_items = MenuItem.objects.filter(category='SOFTDRINKS & JUICES', available=True)
    light_meal_menu_items = MenuItem.objects.filter(category='LIGHT MEALS', available=True)
    beer_and_cider_menu_items = MenuItem.objects.filter(category='BEER & CIDERS', available=True)
    sandwich_menu_items = MenuItem.objects.filter(category='SANDWICHES', available=True)
    dessert_menu_items = MenuItem.objects.filter(category='DESSERT', available=True)
    return render(request, 'registration/index.html', {
        'special_menu_items': special_menu_items,
        'breakfast_menu_items': breakfast_menu_items,
        'main_course_menu_items': main_course_menu_items,
        'dessert_menu_items': dessert_menu_items,
        'soft_drink_menu_items': soft_drink_menu_items,
        'light_meal_menu_items': light_meal_menu_items,
        'beer_and_cider_menu_items': beer_and_cider_menu_items,
        'sandwich_menu_items': sandwich_menu_items,
    })             

# =============================
# Index View (Protected)
# =============================
@login_required()
def admin_home_view(request):
    return render(request, 'registration/admin_home.html')

# =============================
# About View
def about_view(request):
    return render(request, 'registration/about.html')   

# =============================
# Contact View
def contact_view(request):
    return render(request, 'registration/contact.html')


def about(request):
    return render(request, 'registration/about.html')


# =============================
@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': f"{user.first_name} {user.last_name}",
        'email': user.email,
        'phone': user.profile.phone if hasattr(user, 'profile') else '',
    }
    return render(request, 'registration/profile.html', context)

# =============================
@login_required()
def help_view(request):
    return render(request, 'registration/help.html')

# =============================
@login_required()
def refund_view(request):
    return render(request, 'registration/refund.html')

# ============================= 

