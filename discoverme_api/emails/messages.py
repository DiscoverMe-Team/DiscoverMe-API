import os
from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    """
    Sends a styled welcome email to the user using an external HTML template file.
    """
    subject = "Welcome to DiscoverMe!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'welcome.html')

    # Read the HTML content from the file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_message = f.read()
    except FileNotFoundError:
        print(f"Failed to find welcome.html in {current_dir}")
        return

    # Replace placeholders in the HTML template with dynamic values
    html_message = html_message.replace('{{ username }}', user.username)
    html_message = html_message.replace('{{ login_url }}', 'https://discovermeapp.com/login')

    # Fallback plain-text content
    plain_message = f"Hi {user.username},\n\nThank you for joining DiscoverMe! Log in at https://discovermeapp.com/login."

    # Send the email
    send_mail(
        subject=subject,
        message=plain_message,  # Plain-text fallback
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,  # HTML content
        fail_silently=False,
    )
