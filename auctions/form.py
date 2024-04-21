from django import forms
from .models import CATAGORIES_CHOICES

class NewListingForm(forms.Form):

    title = forms.CharField(label="Title",
            widget=forms.TextInput(attrs={'placeholder': 'Title','class': 'form-control'})
            )
    description = forms.CharField(label="Description",
            widget=forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control'},)
            )
    
    ask_price = forms.IntegerField(label="Ask Price(INR)",
            widget=forms.NumberInput(attrs={'placeholder': '100','class': 'form-control'})
            )
    
    category = forms.MultipleChoiceField(label="Category",
        required=True,
        choices=CATAGORIES_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    # category  = models.CharField(max_length=5,choices=CATAGORIES_CHOICES,null=True)
    