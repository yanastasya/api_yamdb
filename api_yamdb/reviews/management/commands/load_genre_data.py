from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genre


ALREDY_LOADED_ERROR_MESSAGE = """
Перед загрузкой данных из CSV-файла:
1.Удалите файл db.sqlite3, чтобы очистить базу данных. 
2. Примените миграци `python manage.py migrate`,
чтобы создать новую пустую БД.
"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Загрузка данных из genre.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Genre.objects.exists():
            print('Данные уже загружены.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return            
        
        print("Загрузка данных genre.")


        for row in DictReader(open('./genre.csv')):
            genre=Genre(id=row['id'], name=row['name'], slug=row['slug'])  
            genre.save()

        print("Загрузка данных genre успешно завершена.")    