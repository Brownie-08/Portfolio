from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form for contact page submissions"""
    
    # Add honeypot field for spam protection
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Leave this field empty"
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True,
                'maxlength': 100
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True,
                'maxlength': 200
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 6,
                'required': True,
                'maxlength': 2000
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set all fields as required
        for field in self.fields.values():
            if field != self.fields['honeypot']:
                field.required = True
                
        # Add custom help text
        self.fields['name'].help_text = "Enter your full name"
        self.fields['email'].help_text = "We'll never share your email with anyone else"
        self.fields['subject'].help_text = "Brief description of your inquiry"
        self.fields['message'].help_text = "Please provide details about your message"
    
    def clean_honeypot(self):
        """Check honeypot field for spam protection"""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError("Spam detected!")
        return honeypot
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise forms.ValidationError("Name can only contain letters and spaces.")
        return name.title()  # Capitalize properly
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        # Use Django's email validator
        validator = EmailValidator()
        try:
            validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
            
        return email
    
    def clean_subject(self):
        """Validate subject field"""
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 5:
            raise forms.ValidationError("Subject must be at least 5 characters long.")
        return subject
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        
        # Check for spam-like content (basic check)
        spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'million dollars']
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in spam_keywords):
            raise forms.ValidationError("Your message appears to contain spam content.")
            
        return message
