#* Marko Dasic 2022/0731

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Hobby)
admin.site.register(Message)
admin.site.register(Chats)
admin.site.register(Payment)
admin.site.register(Report)
admin.site.register(Suspension)
