from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.utils.html import strip_tags
from datetime import datetime
import requests

def send_login_thankyou_email(user_email):
    # Get current date and time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get user location (based on server IP, or you can customize)
    try:
        ip_info = requests.get('https://ipinfo.io/json').json()
        city = ip_info.get('city', 'Unknown City')
        country = ip_info.get('country', 'Unknown Country')
        location = f"{city}, {country}"
    except:
        location = "Unknown Location"

    # Email content
    subject = 'Thank You for Logging In - Yatra Bytes 🚕'
    html_message = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #2575fc;">Thank You for Logging In!</h1>
            <p><strong>🕒 Date & Time:</strong> {current_time}</p>
            <p><strong>📍 Location:</strong> {location}</p>
            <p style="margin-top: 20px;">We are excited to have you back at Yatra Bytes! 🚕✨</p>
        </div>
    """
    plain_message = strip_tags(html_message)
    from_email = 'yourcompanyemail@gmail.com'  # Your sender Gmail

    # Send Email
    send_mail(
        subject,
        plain_message,
        from_email,
        [user_email],  # Receiver is dynamic user email
        html_message=html_message,
        fail_silently=False,
    )

def homepage(request):
    return render(request, "index.html")

def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                send_login_thankyou_email(email)
                request.session['user_id'] = user.id
                return redirect('profile')  # or wherever you want
            else:
                return render(request, 'login.html', {'error': 'Invalid Password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})

    return render(request, 'login.html')
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        # Save User with hashed password
        user = User(
            full_name=full_name,
            email=email,
            password=make_password(password)  # Hash the password here
        )
        user.save()
        return redirect('login')

    return render(request, 'register.html')


@staff_member_required
def admin_dashboard(request):
    return render(request, 'dashboard.html')

