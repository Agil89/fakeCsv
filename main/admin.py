from django.contrib import admin
from main.models import SchemaColumns,Schema,Types
# Register your models here.
admin.site.register(Schema)
admin.site.register(SchemaColumns)
admin.site.register(Types)