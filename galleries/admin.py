from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from sorl.thumbnail.admin import AdminImageMixin as SorlAdminImageMixin
from django.contrib import messages
from .models import *

class AdminImageWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        output = super(AdminImageWidget, self).render(name, value, attrs)
        if value:
            output = (
                u'<div>'
                u'<a style="display:block;margin:0 0 10px" target="_blank" href="%(url)s">'
                u'<img src="%(url)s" width="%(width)spx"></a></div>%(output)s'
                ) % dict(width=100, output=output, url=value)
        return mark_safe(output)

class AdminImageMixin(SorlAdminImageMixin):
    """
    This is a mix-in for ModelAdmin subclasses to make ``ImageField`` show nicer
    form class and widget
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_link':
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(AdminImageMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)

class PhotoInline(AdminImageMixin, admin.TabularInline):
    model = Photo
    fields = ('image_link', 'image','title', 'slug')
    prepopulated_fields = {"slug": ("title",)}

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", 'slug', "created", 'modified', 'is_published', 'video_link')
    search_fields = ['title']
    list_filter = ('is_published', 'created', 'modified')
    prepopulated_fields = {"slug": ("title",)}

def publish(modeladmin, request, queryset):
    count = queryset.update(is_published=True)
    messages.info(request, 'Successfully published %s galleies' % count)
publish.description = 'Publish selected.'

def unpublish(modeladmin, request, queryset):
    count = queryset.update(is_published=False)
    messages.info(request, 'Successfully un-published %s galleies' % count)
publish.description = 'Un-Publish selected.'

class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", 'slug', "created", "modified", 'is_published', 'preview')
    search_fields = ['title']
    list_filter = ('is_published', 'created', 'modified')
    inlines = [PhotoInline]
    prepopulated_fields = {"slug": ("title",)}
    actions = [unpublish, publish]


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
