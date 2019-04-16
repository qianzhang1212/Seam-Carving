from django import forms
from django.forms.widgets import Select, NumberInput, ClearableFileInput

class ProcessForm(forms.Form):
    input_image = forms.FileField(label="Input image", required=True)
    operation = forms.ChoiceField(label="Operation", required=True)
    mask_image = forms.FileField(label="Mask image", required=False)
    new_width = forms.IntegerField(label="New width", required=False)
    new_height = forms.IntegerField(label="New height", required=False)
    
    # input_image = forms.FileField(label="Input image",
    #                            required=True,
    #                            widget=ClearableFileInput(attrs={
    #                                'id': 'input-upload',
    #                                'tabindex': '1'
    #                            }))
    # operation = forms.ChoiceField(label="Operation",
    #                            required=True,
    #                            widget=Select(attrs={
    #                                'name': 'operation',
    #                                'id': 'operation',
    #                                'tabindex': '2',
    #                                'class': 'form-control'
    #                            }))
    # mask_image = forms.FileField(label="Mask image",
    #                            required=False,
    #                            widget=ClearableFileInput(attrs={
    #                                'id': 'mask-upload',
    #                                'tabindex': '3'
    #                            }))
    # new_width = forms.IntegerField(label="New width",
    #                            required=False,
    #                            widget=NumberInput(attrs={
    #                                'name': 'new-width',
    #                                'id': 'new-width',
    #                                'tabindex': '4',
    #                                'class': 'form-control'
    #                            }))
    # new_height = forms.IntegerField(label="New height",
    #                            required=False,
    #                            widget=NumberInput(attrs={
    #                                'name': 'new-height',
    #                                'id': 'new-height',
    #                                'tabindex': '5',
    #                                'class': 'form-control'
    #                            }))
    
