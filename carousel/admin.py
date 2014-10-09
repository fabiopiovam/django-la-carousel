from django.contrib import admin

from carousel.models import Photo, Carousel
from adminsortable.admin import SortableAdmin, SortableTabularInline

class PhotoInline(SortableTabularInline):
    template = 'adminsortable/edit_inline/tabular.html'
    model = Photo
    extra = 1

class CarouselAdmin(SortableAdmin):
    list_display = ('type','owner','published')
    list_filter = ['type','published']
    search_fields = ['photo__title','photo__description','photo__link','owner__username']
    
    fieldsets = [
        (None,   {'fields': ['type','published']}),
    ]
    
    inlines = [PhotoInline]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner_id', None) is None:
            obj.owner_id = request.user.id
        obj.save()

admin.site.register(Carousel, CarouselAdmin)