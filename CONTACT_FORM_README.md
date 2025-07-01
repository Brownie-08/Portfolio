# Contact Form System

This Django portfolio project includes a fully functional contact form system with email notifications.

## Features

### ContactForm (ModelForm)
- **Model**: `ContactMessage` - stores all contact form submissions
- **Fields**: name, email, subject, message
- **Validation**: 
  - Custom validation for each field
  - Spam protection with honeypot field
  - Email validation
  - Message length validation
  - Basic spam keyword detection
- **Security**: CSRF protection, field sanitization

### ContactView (FormView)
- **Template**: `portfolio/contact.html`
- **Success handling**: Shows success message and redirects
- **Error handling**: Shows error messages for form validation failures
- **Email notifications**: Sends emails to admin and auto-reply to sender

### Email Notification System
- **Admin notification**: Detailed email to portfolio owner
- **Auto-reply**: Thank you message to form sender
- **Configuration**: Flexible email settings via environment variables
- **Error handling**: Graceful fallback if email sending fails

## Setup Instructions

### 1. Environment Configuration

Copy `.env.example` to `.env` and configure your email settings:

```bash
cp .env.example .env
```

### 2. Email Configuration Options

#### Development (Console Backend)
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Emails will be printed to the console instead of being sent.

#### Production with Gmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_EMAIL=your-email@gmail.com
```

#### Production with SendGrid
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL=admin@yourdomain.com
```

### 3. Contact Form Settings

```env
# Email where contact form submissions are sent
CONTACT_EMAIL=your-email@example.com

# Whether to send auto-reply to form senders
SEND_AUTO_REPLY=True

# Subject prefix for admin emails
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact] 
```

### 4. Database Migration

Make sure to run migrations for the ContactMessage model:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Test Email Configuration

Use the included management command to test your email setup:

```bash
# Test with default email
python manage.py test_email

# Test with specific email
python manage.py test_email --to test@example.com
```

## Usage

### Form Integration

The contact form is automatically available at `/contact/` URL. The form includes:

- **Name field**: Required, minimum 2 characters
- **Email field**: Required, must be valid email format
- **Subject field**: Required, minimum 5 characters  
- **Message field**: Required, minimum 10 characters
- **Honeypot field**: Hidden spam protection

### Form Processing

When a form is submitted:

1. **Validation**: All fields are validated according to the rules
2. **Storage**: Valid submissions are saved to the database
3. **Admin Email**: Detailed notification sent to `CONTACT_EMAIL`
4. **Auto-reply**: Thank you email sent to form submitter (if enabled)
5. **Success Message**: User sees confirmation message
6. **Redirect**: User is redirected back to contact form

### Email Templates

#### Admin Notification Format:
```
Subject: [Portfolio Contact] User's Subject

New Contact Form Submission
============================

From: John Doe
Email: john@example.com
Subject: Interested in your services
Submitted: 2024-01-15 14:30:25

Message:
----------------------------------------
I would like to discuss a potential project...
----------------------------------------

You can reply directly to john@example.com
```

#### Auto-reply Format:
```
Subject: Thank you for contacting me!

Hi John Doe,

Thank you for reaching out through my portfolio website! 

I have received your message about "Interested in your services" and will get back to you as soon as possible, typically within 24-48 hours.

Here's a copy of your message for your records:
----------------------------------------
I would like to discuss a potential project...
----------------------------------------
```

## Model Structure

### ContactMessage Model
```python
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Custom validation for all form fields
- **Spam Protection**: Honeypot field to catch automated submissions
- **Rate Limiting**: Consider adding rate limiting in production
- **Email Security**: Proper email header sanitization

## Customization

### Custom Validation
Add custom validation methods to the `ContactForm` class in `forms.py`.

### Email Templates
Modify the email message formats in the `send_email_notification` and `send_auto_reply` methods in `views.py`.

### Styling
The form uses Bootstrap classes. Customize the CSS classes in the form widget definitions.

## Troubleshooting

### Email Not Sending
1. Check your email configuration in `.env`
2. Run `python manage.py test_email` to verify setup
3. Check Django logs for error messages
4. Verify email provider settings (Gmail app passwords, SendGrid API keys, etc.)

### Form Validation Errors
1. Check the browser console for JavaScript errors
2. Verify CSRF token is present in form
3. Check Django logs for server-side validation errors

### Development Testing
Use the console email backend for development:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This will print emails to the terminal instead of sending them.

## Production Considerations

1. **Email Provider**: Use a reliable email service (SendGrid, Mailgun, AWS SES)
2. **Rate Limiting**: Implement rate limiting to prevent spam
3. **Monitoring**: Monitor email delivery and form submissions
4. **Backup**: Regularly backup contact form submissions
5. **SSL/TLS**: Ensure your site uses HTTPS for form security
