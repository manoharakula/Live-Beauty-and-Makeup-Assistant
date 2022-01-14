from django.contrib import admin

# Register your models here.
from .models import FaceModel , EyesModel, LooksModel,LipsModel ,ColorsPallete
 
admin.site.register(FaceModel)
admin.site.register(EyesModel)
admin.site.register(LipsModel)
admin.site.register(LooksModel)
admin.site.register(ColorsPallete)
