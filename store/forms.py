from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class RegisterForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'stock']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'})
        }