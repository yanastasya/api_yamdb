from django.contrib import admin
from .models import Title, Genre, Categorie, TitleGenre


class TitlesAdmin(admin.ModelAdmin):

    list_display = (
        'pk', 'name', 'year', 'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitlesAdmin)
admin.site.register(Genre)
admin.site.register(Categorie)
admin.site.register(TitleGenre)
