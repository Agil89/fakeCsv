from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from main.models import Types, Schema, SchemaColumns
from django.forms import modelformset_factory, inlineformset_factory

USER_MODEL = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Username'),
        'autofocus': True
    }), )
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


# class TypesForm(forms.ModelForm):
#     CHOICES = (
#         ('job', 'Job'),
#         ('email', 'Email'),
#         ('company name', 'Company name'),
#         ('integer', 'Integer'),
#         ('text', 'Text'),
#     )
#     types = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={
#         'class':'form-control'
#     }))
#     class Meta:
#         model=Types
#         fields=(
#             'types',
#         )

class TypesForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(TypesForm, self).__init__(*args, **kargs)

    class Meta:
        model = Types
        fields = '__all__'


class SchemaColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumns
        fields = '__all__'




class SchemaForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(UpdateSchemaForm, self).__init__(*args, **kwargs)
    #     self.fields['schemaColumns'].queryset = SchemaColumns.objects
    class Meta:
        model = Schema
        fields = ('title','user',)
        widgets ={
            'title':forms.TextInput(attrs={
                'class':'form-control'
            })
        }
# SchemaFormFactory = inlineformset_factory(Schema, SchemaColumns, fields=('column_name','column_type','order','range'), can_delete=False)


# class UpdateSchemaForm(forms.ModelForm):
#     template_name = 'update.html'
#     model = Schema
#     form_class = SchemaForm
#     # success_url = reverse_lazy('billing_report')
#     # success_message = 'Billing Updated Successfully.'
