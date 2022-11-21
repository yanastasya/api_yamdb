from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import TitleGenre, Title, Genre


ALREDY_LOADED_ERROR_MESSAGE = """
Перед загрузкой данных из CSV-файла:
1.Удалите файл db.sqlite3, чтобы очистить базу данных. 
2. Примените миграци `python manage.py migrate`,
чтобы создать новую пустую БД.
"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Загрузка данных из titlegenre.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if TitleGenre.objects.exists():
            print('Данные уже загружены.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return            
        
        print("Загрузка данных genre.")


        for row in DictReader(open('./genre_title.csv')):
            genretitle=TitleGenre(id=row['id'], title=Title.objects.get(id=row['title_id']), genre=Genre.objects.get(id=row['genre_id']))
            genretitle.save()

        print("Загрузка данных genretitle успешно завершена.")    