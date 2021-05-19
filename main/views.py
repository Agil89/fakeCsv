from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from fakeCsv.settings import MEDIA_URL
from main.forms import LoginForm, TypesForm, SchemaForm
from main.models import Types, Schema, SchemaColumns
from django.views.generic.edit import FormMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django import forms
import csv
from main.tasks import generate_csv


# Create your views here.

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        schemas = Schema.objects.filter(user=self.request.user)
        context = super().get_context_data(*args, **kwargs)
        if schemas:
            context['schemas'] = schemas
        return context


class CreateCsvView(View, FormMixin):
    def post(self, request):
        name = request.POST.get('name')
        column_names = request.POST.getlist('column-name')
        types = request.POST.getlist('type')
        orders = request.POST.getlist('order')
        froms = request.POST.getlist('from')
        tos = request.POST.getlist('to')
        Schema.objects.create(
            user=request.user,
            title=name
        )
        count = 0
        for x in range(len(column_names)):
            if types[x] == 'integer':
                SchemaColumns.objects.create(
                    schema=Schema.objects.filter(title=name).first(),
                    column_name=column_names[x],
                    column_type=types[x],
                    order=orders[x],
                    range=froms[count] + '-' + tos[count]
                )
                count += 1
            else:
                SchemaColumns.objects.create(
                    schema=Schema.objects.filter(title=name).first(),
                    column_name=column_names[x],
                    column_type=types[x],
                    order=orders[x],
                )

        return redirect('home')

    def get(self, request):
        form = TypesForm()
        context = {
            'types': form
        }
        return render(request, 'create.html', context)


class DownloadView(View):
    template_name = 'download.html'

    def post(self, *args, **kwargs):
        row_count = self.request.POST.get('value')
        user = self.request.user
        schemas = Schema.objects.filter(user__id=user.id)[:int(row_count)]
        generate_csv(row_count,user)
        context = {
            'schemas': schemas
        }
        return redirect('download')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        schemas = Schema.objects.filter(user__id=user.id)
        context = {
            'schemas': schemas
        }
        return render(self.request, 'download.html', context)


class TypeList(APIView):
    def get(self, request):
        all_types = Types.type_choice

        return Response({
            'all_types': all_types,
        })


class SchemaDeleteView(DeleteView):
    model = Schema
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class SchemaUpdateView(View):
    form_class = SchemaForm
    model = Schema
    template_name = 'update.html'

    def get(self, request, *args, **kwargs):
        types = TypesForm()
        schema_id = kwargs.get('pk')
        schema = Schema.objects.get(pk=schema_id)
        SchemaFormSet = inlineformset_factory(Schema, SchemaColumns, fields=('column_name', 'column_type', 'order',),
                                              extra=0)
        formset = SchemaFormSet(instance=schema)
        form = SchemaForm(instance=schema)
        return render(request, 'update.html', {'formset': formset, 'form': form, 'types': types})

    def post(self, request, *args, **kwargs):
        schema_id = kwargs.get('pk')
        schema = Schema.objects.get(pk=schema_id)
        SchemaFormSet = inlineformset_factory(Schema, SchemaColumns, fields=('column_name', 'column_type', 'order',),
                                              extra=0, widgets={
                'column-name': forms.TextInput(attrs={
                    'class': 'form-control'
                }),
                'order': forms.TextInput(attrs={
                    'class': 'form-control'
                })
            })
        formset = SchemaFormSet(request.POST, instance=schema)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            return HttpResponseRedirect(reverse_lazy('home'))
        return HttpResponseRedirect(reverse_lazy('home'))



