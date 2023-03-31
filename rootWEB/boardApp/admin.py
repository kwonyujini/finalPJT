from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(user_tbl)
admin.site.register(board_tbl)