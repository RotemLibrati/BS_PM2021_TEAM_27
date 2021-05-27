from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Media)
admin.site.register(Child)
admin.site.register(Score)
admin.site.register(Kindergarten)
admin.site.register(Notification)
admin.site.register(Note)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question','answer')

admin.site.register(FAQ,FAQAdmin)
admin.site.register(Video)

