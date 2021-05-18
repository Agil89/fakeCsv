from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,DeleteView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView
from main.forms import LoginForm,TypesForm,SchemaForm,SchemaFormFactory
from main.models import Types,Schema,SchemaColumns
from django.views.generic.edit import FormMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.forms import inlineformset_factory



# Create your views here.

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'





class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,*args, **kwargs):
        print(Schema.objects.last().molumns())
        schemas = Schema.objects.filter(user=self.request.user)
        context = super().get_context_data(*args, **kwargs)

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
    def get(self, request):
        context = {
            'types': 'types'
        }
        return render(request, 'download.html', context)

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


class SchemaUpdateView(UpdateView):
  model = Schema
  form_class = SchemaForm
  template_name = 'update.html'

  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    schema_line_item = SchemaFormFactory(instance = self.object)
    return self.render_to_response(self.get_context_data(form = form, schema_line_item_form = schema_line_item))

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    schema_line_item_form = SchemaFormFactory(self.request.POST, instance=self.object)

    if (form.is_valid() and schema_line_item_form.is_valid()):
      return self.form_valid(form, schema_line_item_form)
    return self.form_invalid(form, schema_line_item_form)

  def form_valid(self, form, expense_line_item_form):
    self.object = form.save()
    expense_line_item_form.instance = self.object
    expense_line_item_form.save()
    return HttpResponseRedirect(self.get_success_url())

  def form_invalid(self, form, schema_line_item_form):
    return self.render_to_response(self.get_context_data(form=form, schema_line_item_form=schema_line_item_form))
