from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ContactUs

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile

    """
    can_delete = False
    fk_name = 'user'
    fields = ['user', 'nric', 'state']
    readonly_fields = ['nric']
    exclude = ['country', ]
    list_display = ('user', 'nric', 'email')
    list_filter = ('user',)
    search_fields = ('user', 'nric')
    list_per_page = 20
    """

class ContactUsAdmin(admin.ModelAdmin):
    class Meta:
        model = ContactUs

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileAdmin]

    """
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
    """

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
