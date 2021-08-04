from django import forms
from django.forms import ModelForm
from . import models as mod

# class CreateTicket(forms.Form):
#     title = forms.CharField(max_length=150)
#     description = forms.CharField(widget=forms.Textarea)
    # image = forms.ImageField()


class CreateTicket(ModelForm):
    class Meta:
        model = mod.Ticket
        # fields = "__all__"
        fields = ['title', 'description', 'image']
        exclude = ['user', 'time_created']


class CreateReview(ModelForm):
    CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = mod.Review
        # fields = "__all__"
        fields = ['rating', 'headline', 'body']
        exclude = ['ticket', 'user', 'time_created']
