from celery import shared_task
from main.models import Schema
import csv

@shared_task
def generate_csv(row_count,user):
    schemas = Schema.objects.filter(user__id=user.id)[:int(row_count)]
    for schema in list(schemas):
        with open(f'media/{schema.title}.csv', 'w') as csvfile:
            for x in sorted(schema.molumns().values_list('column_name', 'column_type', 'order')):
                row = []
                for e in x:
                    writer = csv.writer(csvfile)
                    row += [e]
                writer.writerow(row)
        a = Schema.objects.get(id=schema.id)
        a.url = f'media/{schema.title}.csv'
        a.save()
    return True