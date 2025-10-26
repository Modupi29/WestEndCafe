from django import forms
from .models import PaymentProof

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # The 'update' field indicates whether to update the quantity or add to it

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['proof_file']

    def clean_proof_file(self):
        file = self.cleaned_data.get('proof_file')
        if file:
            if not file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("File must be PDF or JPG/PNG.")
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size must be under 5MB.")
        return file