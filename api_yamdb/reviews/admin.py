from django.contrib import admin
from .models import Titles, Genre, Categories, Rewiews, Comments


class TitlesAdmin(admin.ModelAdmin):

    list_display = (
        'pk', 'name', 'categories', 'genre', 'year', 'description',
    )
    search_fields = ('name', 'categories', 'genre',)
    list_filter = ('name', 'categories', 'genre',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genre)
admin.site.register(Categories)
admin.site.register(Rewiews)
admin.site.register(Comments)
