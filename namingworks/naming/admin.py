from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget

class SummernoteWidgetWithCustomToolbar(SummernoteWidget):
    def template_contexts(self):
        contexts = super(SummernoteWidgetWithCustomToolbar, self).template_contexts()
        contexts['width'] = '960px'
        return contexts

class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {models.TextField: {'widget': SummernoteWidgetWithCustomToolbar}}

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

