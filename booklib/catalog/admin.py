from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    list_filter = ('last_name',)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

"""
--Version 1
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    #list_display = ('id','book.author')
    list_filter = ('status', 'due_back')

    fieldsets = (
            (None, {
                'fields': ('book','imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back')
            }),
        )
"""

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
            (None, {
                'fields': ('book','imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back', 'borrower')
            }),
        )

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


#admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
#admin.site.register(BookInstance)




