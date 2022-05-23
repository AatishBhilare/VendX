from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, FileInput, NumberInput

from vmmanager.models import VmItem


class EditVmItemForm(forms.ModelForm):
    class Meta:
        model = VmItem
        fields = ['item_name', 'item_price', 'item_img', 'item_inv']

        widgets = {

            "item_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "item_inv": NumberInput(
                attrs={
                    "class": "form-control"
                }),
            "item_price": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "item_img": FileInput(
                attrs={

                }),

        }

    def clean_item_img(self):
        item_img = self.cleaned_data['item_img']
        if item_img:
            return item_img
        else:
            item_img = 'emptyfile'
            return item_img

    def clean_item_inv(self):
        item_inv = self.cleaned_data['item_inv']
        if item_inv > 10:
            raise ValidationError("Vending Machine Have only 10 Slots")
        else:
            return item_inv
