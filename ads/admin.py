from django.contrib import admin
from ads.models import Ad, Fav


class AdAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')


admin.site.register(Ad, AdAdmin)
admin.site.register(Fav)
