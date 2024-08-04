import json 
from django.core.management.base import BaseCommand
from credit_.models import Credit_score


class Command (BaseCommand):
    help = 'Import external JSON file data Django batabase'
    
    def handle(self, *args, **kwargs):
        with open (r"C:\Users\sopan\Desktop\jupyter\All dataset\Credit score prediction\credit_score_\json_file2.json", "r", encoding='utf8') as file:
            data = json.load(file)
            print(data)
        