from django import forms


class StyleForm(forms.Form):
    style_name = forms.CharField(required=True)


class ChoreographerForm(forms.Form):
    choreographer_name = forms.CharField(required=True)
    style = forms.ChoiceField(choices=[], required=True)

    def update_choices(self, choices):
        self.fields['style'].choices = choices


class DanceSchoolForm(forms.Form):
    # Fields: name, address, phone
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    # Phone number: +{code} 123 456 78 90
    phone = forms.RegexField(regex="^\+\d{1,3} \d{3} \d{3} \d{2} \d{2}$", required=True, help_text="Format: +7 123 456 78 90")

class EditDanceSchoolForm(forms.Form):
    # Fields: name, address, phone
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    # Phone number: +{code} 123 456 78 90
    phone = forms.RegexField(regex="^\+\d{1,3} \d{3} \d{3} \d{2} \d{2}$", required=False, help_text="Format: +{code} 123 456 78 90")

