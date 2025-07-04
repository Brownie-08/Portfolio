# Gmail Setup Guide for Portfolio Contact Notifications

## 📧 **Email Notifications Setup**

This guide will help you set up Gmail to receive contact form submissions directly on your mobile device.

---

## 🔧 **Step 1: Gmail App Password Setup**

### **1.1 Enable 2-Factor Authentication**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under **Signing in to Google**, click **2-Step Verification**
4. Follow the setup process to enable 2FA

### **1.2 Generate App Password**
1. Go back to **Security** settings
2. Under **Signing in to Google**, click **App passwords**
3. Select **Mail** as the app
4. Select **Other (Custom name)** as the device
5. Enter "Portfolio Website" as the name
6. Click **Generate**
7. **SAVE THE 16-CHARACTER PASSWORD** - you'll need this for Django

---

## 🛠️ **Step 2: Update Your .env File**

Replace your current email settings in `.env` with:

```env
# Gmail SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Contact form settings
CONTACT_EMAIL=your-email@gmail.com
SEND_AUTO_REPLY=True
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact] 
```

**Replace:**
- `your-email@gmail.com` with your actual Gmail address
- `your-16-character-app-password` with the app password from Step 1.2

---

## 📱 **Step 3: Mobile Gmail App Setup**

### **Ensure Notifications Are Enabled:**
1. Open **Gmail app** on your mobile device
2. Tap **Menu** (☰) → **Settings**
3. Select your email account
4. Tap **Notifications**
5. Choose **All new mail** or **High priority only**
6. Enable **Sound**, **Vibrate**, and **Light** as desired

### **Label Filter (Optional but Recommended):**
1. Open Gmail on your computer
2. Go to **Settings** → **Filters and Blocked Addresses**
3. Click **Create a new filter**
4. In **Subject** field, enter: `[Portfolio Contact]`
5. Click **Create filter**
6. Check **Apply the label** and create a new label called "Portfolio"
7. Check **Never send it to Spam**
8. Click **Create filter**

---

## 🧪 **Step 4: Test Email Configuration**

Run this command to test your email setup:

```bash
python manage.py shell -c "
from django.core.mail import send_mail
from django.conf import settings
try:
    send_mail(
        'Portfolio Email Test',
        'This is a test email from your Django portfolio.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.CONTACT_EMAIL],
        fail_silently=False,
    )
    print('✅ Email sent successfully!')
except Exception as e:
    print(f'❌ Email failed: {e}')
"
```

---

## 📧 **Step 5: Test Contact Form**

1. Go to your portfolio contact page: http://127.0.0.1:8000/contact/
2. Fill out and submit the contact form
3. Check your Gmail (both on mobile and computer)
4. You should receive:
   - **Admin notification** with the contact details
   - **Auto-reply** sent to the form submitter

---

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Authentication failed" error:**
   - Double-check your app password (16 characters, no spaces)
   - Ensure 2FA is enabled on your Google account

2. **"SMTPAuthenticationError":**
   - Verify your Gmail address is correct
   - Make sure you're using the app password, not your regular password

3. **Emails going to spam:**
   - Set up the Gmail filter from Step 3
   - Add your own email to contacts

4. **No mobile notifications:**
   - Check Gmail app notification settings
   - Ensure the app has notification permissions in phone settings

---

## 📋 **Email Templates**

Your contact form will send two emails:

### **Admin Notification (to you):**
```
Subject: [Portfolio Contact] Contact Subject Here
From: your-email@gmail.com
To: your-email@gmail.com

New Contact Form Submission
============================

From: Visitor Name
Email: visitor@email.com
Subject: Their Subject
Submitted: 2025-07-03 10:30:00

Message:
----------------------------------------
Their message content here
----------------------------------------

You can reply directly to visitor@email.com
```

### **Auto-Reply (to visitor):**
```
Subject: Thank you for contacting me!
From: your-email@gmail.com
To: visitor@email.com

Hi [Visitor Name],

Thank you for reaching out through my portfolio website! 

I have received your message about "[Subject]" and will get back to you as soon as possible, typically within 24-48 hours.

Best regards,
[Your Name]
```

---

## 🎯 **Dashboard Message Management**

Enhanced dashboard features:
- ✅ **Filter messages** by read/unread status
- ✅ **Search** through names, emails, subjects, messages
- ✅ **Bulk actions** - mark multiple messages as read/unread
- ✅ **Delete old messages** in bulk
- ✅ **Pagination** for large volumes of messages
- ✅ **Visual indicators** for unread messages

**Access at:** http://127.0.0.1:8000/dashboard/messages/

---

## 🔐 **Security Best Practices**

1. **Never share your app password**
2. **Use environment variables** (`.env` file) for sensitive data
3. **Revoke app passwords** if you suspect they're compromised
4. **Regularly review** Google account security settings
5. **Keep your `.env` file** out of version control (already in .gitignore)

---

## 🚀 **Production Deployment Notes**

When deploying to production:
1. Set environment variables on your hosting platform
2. Consider using a dedicated email service like SendGrid or AWS SES for higher volume
3. Set up proper SPF/DKIM records for your domain
4. Monitor email delivery rates and bounces

---

**You're all set! Your portfolio will now send email notifications directly to your Gmail, which you can receive on your mobile device instantly! 📱✉️**
