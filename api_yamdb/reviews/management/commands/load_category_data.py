from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from reviews.models import Categorie


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Загрузка данных из category.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Categorie.objects.exists():
            print('Данные уже загружены.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Загрузка категорий.")


        #Code to load the data into database
        for row in DictReader(open('./static/data/category.csv', encoding='utf-8')):
            categorie=Categorie(id=row['id'], name=row['name'], slug=row['slug'])  
            categorie.save()