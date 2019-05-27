from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Restaurant, Dish, RestaurantReview

#@admin.register(User) or admin.site.register(User, UserAdmin)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no username field.
    The forms to add and change user instances """
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(RestaurantReview)
