from django.forms import ModelForm
from app.models import *
from django import forms
from inventory.models import *



class BillingForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset=Cabinorder.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class AddReviews(ModelForm):
    class Meta: 
        model = Review
        fields = '__all__'

class CabinForm(forms.ModelForm):
    class Meta:
        model = Cabin
        fields = ['cabinnumber', 'photo']
        widgets = {
            'cabinnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cabin number'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class AddCabinOrderWithCabinForm(forms.ModelForm):
    class Meta:
        model = Cabinorder
        fields = ['cabin', 'product', 'quantity']
        widgets = {
            'cabin': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        }

class AddCabinOrderWithoutCabinForm(forms.ModelForm):
    class Meta:
        model = Cabinorder
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        }



class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UpdateorderplacedForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['quantity', 'customer', 'status']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select status'}),
        }

class UpdateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'comment', 'rate', 'status' ]
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your comment'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your rate'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select status'}),
        }

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'composition', 'category', 'product_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter selling price'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discounted price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter product description'}),
            'composition': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter product composition'}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select category'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class UpdateCabinForm(forms.ModelForm):
    class Meta:
        model = Cabin
        fields = ['cabinnumber', 'photo']
        widgets = {
            'cabinnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cabin number'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }





