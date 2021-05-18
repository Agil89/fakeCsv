from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,DeleteView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView
from main.forms import LoginForm,TypesForm,SchemaForm
from main.models import Types,Schema,SchemaColumns
from django.views.generic.edit import FormMixin, BaseUpdateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.forms import modelformset_factory, inlineformset_factory
from django import forms



# Create your views here.

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'





class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,*args, **kwargs):
        schemas = Schema.objects.filter(user=self.request.user)
        context = super().get_context_data(*args, **kwargs)
        if schemas:
            context['schemas'] = schemas
        return context

class CreateCsvView(View,FormMixin):
    def post(self,request):
        name = request.POST.get('name')
        column_names = request.POST.getlist('column-name')
        types = request.POST.getlist('type')
        orders = request.POST.getlist('order')
        froms = request.POST.getlist('from')
        tos = request.POST.getlist('to')
        Schema.objects.create(
            user=request.user,
            title = name
        )
        count=0
        for x in range(len(column_names)):
            if types[x]=='integer':
                SchemaColumns.objects.create(
                    schema=Schema.objects.filter(title=name).first(),
                    column_name=column_names[x],
                    column_type=types[x],
                    order=orders[x],
                    range=froms[count] + '-' + tos[count]
                )
                count +=1
            else:
                SchemaColumns.objects.create(
                    schema = Schema.objects.filter(title=name).first(),
                    column_name=column_names[x],
                    column_type=types[x],
                    order=orders[x],
                )

        return redirect('home')

    def get(self,request):
        form = TypesForm()
        context={
            'types':form
        }
        return render(request, 'create.html', context)

class DownloadView(View):
    template_name = 'download.html'

    def post(self,*args,**kwargs):
        row_count = self.request.POST.get('value')
        user = self.request.user
        schemas = Schema.objects.filter(user__id=user.id)[:int(row_count)]
        for schema in list(schemas):
            print(schema.molumns())
        # for schema in schemas:
            # schemaColumns = schema.select_related('schemaColumns__column_name','schemaColumns__column_type','schemaColumns__order')
            # print(schemaColumns.values('title','schemaColumns__column_name','schemaColumns__column_type','schemaColumns__order'))
        # for schema in schemas:
        #     print(schema.schemaColumns.column_name.value())
        # for schema in schemas:
        #     print(schema.title)
        #     print(schema.schemaColumns__column_name)
            # for e in schema:
            #     print(e)
            # print(list(schema.values()))
            # print(getattr(schema, ('title','schemaColumns__column_name','schemaColumns__column_type','schemaColumns__order')))
            # print(schema.values_list('title','schemaColumns__column_name','schemaColumns__column_type','schemaColumns__order'))
        context = {
            'schemas':schemas
        }
        return render(self.request, 'download.html',context)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        schemas = Schema.objects.filter(user__id=user.id)
        context={
            'schemas':schemas
        }
        return render(self.request, 'download.html',context)



class TypeList(APIView):
    def get(self,request):
        all_types = Types.type_choice

        return Response({
            'all_types': all_types,
        })


class SchemaDeleteView(DeleteView):
    model = Schema
    success_url = reverse_lazy('home')
    # http_method_names = ('get',)

    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

# class SchemaUpdateView(UpdateView):
#     form_class = SchemaForm
#     model = Schema
#     template_name = 'update.html'


# class SchemaUpdateView(UpdateView):
#   model = Schema
#   form_class = SchemaForm
#   template_name = 'update.html'
#
#   def get(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     form_class = self.get_form_class()
#     form = self.get_form(form_class)
#     schema_line_item = SchemaFormFactory(instance = self.object)
#     return self.render_to_response(self.get_context_data(form = form, schema_line_item_form = schema_line_item))
#
#   def post(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     form_class = self.get_form_class()
#     form = self.get_form(form_class)
#     schema_line_item_form = SchemaFormFactory(self.request.POST, instance=self.object)
#
#     if (form.is_valid() and schema_line_item_form.is_valid()):
#       return self.form_valid(form, schema_line_item_form)
#     return self.form_invalid(form, schema_line_item_form)
#
#   def form_valid(self, form, expense_line_item_form):
#     self.object = form.save()
#     expense_line_item_form.instance = self.object
#     expense_line_item_form.save()
#     return HttpResponseRedirect(self.get_success_url())
#
#   def form_invalid(self, form, schema_line_item_form):
#     return self.render_to_response(self.get_context_data(form=form, schema_line_item_form=schema_line_item_form))


class SchemaUpdateView(View):
    form_class = SchemaForm
    model = Schema
    template_name = 'update.html'

    def get(self, request, *args, **kwargs):
        types = TypesForm()
        schema_id = kwargs.get('pk')
        schema = Schema.objects.get(pk=schema_id)
        SchemaFormSet = inlineformset_factory(Schema, SchemaColumns, fields=('column_name','column_type','order',),extra=0)
        formset = SchemaFormSet(instance=schema)
        form = SchemaForm(instance=schema)
        return render(request, 'update.html', {'formset': formset,'form':form,'types':types})

    def post(self,request, *args, **kwargs):
        schema_id = kwargs.get('pk')
        schema = Schema.objects.get(pk=schema_id)
        SchemaFormSet = inlineformset_factory(Schema, SchemaColumns, fields=('column_name', 'column_type', 'order',),
                                              extra=0,widgets ={
            'column-name':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'order':forms.TextInput(attrs={
                'class':'form-control'
            })
        })
        # formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer__id=programmer.id))
        formset = SchemaFormSet(request.POST, instance=schema)
        if formset.is_valid():
            formset.save()
            # instances = formset.save(commit=False)
            # for instance in instances:
            #    instance.programmer_id = programmer.id
            #    instance.save()
        else:
            print(formset.errors)
            return HttpResponseRedirect(reverse_lazy('home'))
        return HttpResponseRedirect(reverse_lazy('home'))


class GenerateDataView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')


        return None
