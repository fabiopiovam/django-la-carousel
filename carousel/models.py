# -*- coding: utf-8 -*-
import random, glob, os, shutil
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

carousel_choices = (
    ('principal', u'Principal (1350px x 563px)'),
)

class Photo(Sortable):
    class Meta(Sortable.Meta):
        verbose_name        = u"imagem"
        verbose_name_plural = u"imagens"
    
    def save(self):
        if self.image:
            if self.id:
                obj_photo = Photo.objects.get(id=self.id)
                if self.image not in [obj_photo.image]:
                    for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
                        os.remove(fl)
            
            super(Photo, self).save()
    
    def delete(self):
        obj_photo = Photo.objects.get(id=self.id)
        super(Photo, self).delete()
        for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
            os.remove(fl)
    
    def get_upload_to_image(self, filename):
        ext = filename[-3:].lower()
        if ext == 'peg': ext='jpeg'        
        return 'carousel/%s/%s_%s.%s' % (self.carousel.id, datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randint(00000,99999)), ext)
    
    def __unicode__(self):
        return u'%s' % self.image
    
    carousel = SortableForeignKey('Carousel')
    image = ThumbnailerImageField(u'Imagem', blank=False, null=False, upload_to = get_upload_to_image, resize_source=dict(size=(1350, 563), sharpen=False, crop="scale"))
    title = models.CharField(u'Título', max_length=50, blank=True, null=True)
    description = models.CharField(u'Descrição', max_length=100, blank=True, null=True)
    link = models.CharField(u'Link', max_length=100, blank=True, null=True)


class CarouselActivatedManager(models.Manager):
    def get_queryset(self):
        return super(CarouselActivatedManager, self).get_queryset().filter(published=True).order_by('-updated_at')


class Carousel(Sortable):
    def __unicode__(self):
        return u'%s' % self.type
    
    class Meta(Sortable.Meta):
        verbose_name = u"carousel"
        
    def delete(self):
        dir = '%s/carousel/%s' % (settings.MEDIA_ROOT, self.id)
        
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    def images_set(self):
        photo = self.photo_set.order_by('order')
        return photo
    
    owner = models.ForeignKey(User, verbose_name=u"Usuário")
    
    type = models.CharField(u'Carousel', max_length=50, choices=carousel_choices)
    published = models.BooleanField(u'Publicado', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    u''' Managers '''
    objects     = models.Manager()
    activated   = CarouselActivatedManager()
