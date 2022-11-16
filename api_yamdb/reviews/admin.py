from django.contrib import admin
from .models import Titles, Genre, Categories, TitlesGenre


class TitlesAdmin(admin.ModelAdmin):

    list_display = (
        'pk', 'name', 'year', 'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genre)
admin.site.register(Categories)
admin.site.register(TitlesGenre)
