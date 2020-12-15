from django import forms


from bottle_shop_app.models import User, Message, Bottle, Comment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'location', 'date_of_birth', 'password', 'prof_photo', 'about')

class BottleForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Bottle
        fields = ('classification', 'vintage', 'varietal', 'producer', 'tasting_notes', 'bottle_photo')