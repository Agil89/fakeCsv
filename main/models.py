from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Types(models.Model):
    type_choice = [
        ('job', 'Job'),
        ('email', 'Email'),
        ('company name', 'Company name'),
        ('integer', 'Integer'),
        ('text', 'Text'),
    ]
    type = models.CharField('Type', max_length=20, choices=type_choice)


class SchemaColumns(models.Model):
    # relations
    schema = models.ForeignKey('Schema', verbose_name='Schema', on_delete=models.CASCADE, related_name='schemaColumns')

    # informations
    column_name = models.CharField('Column name', max_length=50)
    column_type = models.CharField('Type', max_length=50)
    order = models.PositiveSmallIntegerField('Order')
    range = models.CharField('Range', blank=True, null=True, max_length=50)


class Schema(models.Model):
    user = models.ForeignKey(USER_MODEL, verbose_name='Author', on_delete=models.CASCADE, db_index=True)
    title = models.CharField('Title', max_length=50, unique=True)
    created_at = models.DateField(auto_now=True)
    url = models.CharField(max_length=200,blank=True,null=True)


    def molumns(self):
        return self.schemaColumns.all()