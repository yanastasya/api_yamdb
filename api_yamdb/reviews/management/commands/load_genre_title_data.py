from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from reviews.models import Title, Genre, TitleGenre


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
        if TitleGenre.objects.exists():
            print('Данные уже загружены.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Загрузка связей жанров и категорий.")


        #Code to load the data into database
        for row in DictReader(open('./static/data/genre_title.csv')):
            titlegenre=TitleGenre(id=row['id'], title=Title.objects.get(id=row['title_id']), genre=Genre.objects.get(id=row['genre_id']))  
            titlegenre.save()