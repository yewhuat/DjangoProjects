from django import forms
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import ContactUs, UserProfile
from django.utils.safestring import mark_safe
# For ContactUsFormCrispy
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
#from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, Field, InlineRadios, TabHolder, Tab
#from django.core.urlresolvers import reverse




CATEGORY = (
    ('1', u'System01'),
    ('2', u'System02'),
    ('3', u'System03'),
    ('0', u'Others'),
)

class ContactUsForm(forms.ModelForm):
    """
    name = forms.CharField(required=True, max_length=100, help_text='max 100 characters', widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(required=True, max_length=100)
    mobileno = forms.CharField(required=True, max_length=20, label= 'Mobile No.', help_text='max 20 characters')
    subject= forms.CharField(required=True, max_length=255)
    category= forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY, initial= '0', required=True)
    message = forms.CharField(widget=forms.Textarea)
    """
    # Not working
    #category= forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=CATEGORY, initial= '0', required=True)
    category= forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY, initial= '0', required=True)

    class Meta:
        model = ContactUs
        fields = '__all__'
        labels = {
            'mobileno': _('Mobile No.'),
        }
        help_texts = {
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'mobileno': forms.TextInput(attrs={'placeholder': '+60121234567'}),
            'subject': forms.TextInput(attrs={'placeholder': 'OrderNo:99999:Reqeust inspection'}),
            'message': forms.Textarea(attrs={'placeholder': 'Type your details here','cols': 80, 'rows': 10})
        }

class ContactUsFormCrispy(forms.Form):
    """
    Not Working
    """
    name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    mobileno = forms.CharField(required=True, max_length=20, label= 'Mobile No.')
    subject= forms.CharField(required=True, max_length=255)
    #category= forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY, initial= '0', required=True, help_text='<strong>Note:</strong> Please select one category')
    category = forms.TypedChoiceField(
        label="Choose a category",
        choices=CATEGORY,
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='0',
        required=True)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
       #super(ContactUsFormCrispy, self).__init__(*args, **kwargs)
       super().__init__(*args, **kwargs)
       self.helper = FormHelper()
       self.helper.form_id = 'id-ContactUsFormCrispy'
       self.helper.form_method = 'post'
       #self.helper.form_action = reverse('submit_form')
       self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
       self.helper.form_class = 'form-horizontal'
       self.helper.layout = Layout(
           Fieldset('Your Name & Mobile No.',
                    Field('name', placeholder='Your name',
                          css_class="some-class"),
                    Div('email', title="Your ename"),
                    'mobileno', placeholder='+60121234567'),
           Fieldset('Messsage', 'subject', style="color: brown;"),
           InlineRadios('category'),
           Fieldset('Messsage Details', 'message', palceholder="Type your message here "),
                     )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','is_staff','is_active']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

