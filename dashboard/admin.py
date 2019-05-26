from django.contrib import admin

from .models import Project, Attribute, Field, Criterion

admin.site.register(Project)
admin.site.register(Attribute)
admin.site.register(Field)
admin.site.register(Criterion)