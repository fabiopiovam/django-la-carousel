# -*- coding: utf-8 -*-

import random
import glob
import os
import shutil
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

carousel_choices = (
    ('principal', u'Principal (1280px x 377px)'),
)


class Photo(SortableMixin):

    class Meta:
        verbose_name = u"imagem"
        verbose_name_plural = u"imagens"
        ordering = ['photo_order']

    def save(self):
        if self.image:
            if self.id:
                obj_photo = Photo.objects.get(id=self.id)
                if self.image not in [obj_photo.image]:
                    for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,
                                                    obj_photo.image)):
                        os.remove(fl)

            super().save()

    def delete(self):
        obj_photo = Photo.objects.get(id=self.id)
        super().delete()
        for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT, obj_photo.image)):
            os.remove(fl)

    def get_upload_to_image(self, filename):
        ext = filename[-3:].lower()
        if ext == 'peg':
            ext = 'jpeg'
        return 'carousel/%s/%s_%s.%s' % (
            self.carousel.id,
            datetime.now().strftime('%Y%m%d%H%M%S'),
            str(random.randint(00000, 99999)), ext)

    def __str__(self):
        return u'%s' % self.image

    carousel = SortableForeignKey('Carousel', on_delete=models.CASCADE)
    image = ThumbnailerImageField(u'Imagem', blank=False, null=False,
                                  upload_to=get_upload_to_image,
                                  resize_source=dict(size=(1280, 377),
                                                     sharpen=False,
                                                     crop="scale"))
    title = models.CharField(u'Título', max_length=50, blank=True, null=True)
    description = models.CharField(
        u'Descrição', max_length=100, blank=True, null=True)
    link = models.CharField(u'Link', max_length=100, blank=True, null=True)
    photo_order = models.PositiveIntegerField(default=0, editable=False,
                                              db_index=True)


class CarouselActivatedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            published=True).order_by('-updated_at')


class Carousel(SortableMixin):

    def __str__(self):
        return u'%s' % self.type

    class Meta:
        verbose_name = u"carousel"
        ordering = ['carousel_order']

    def delete(self):
        dir = '%s/carousel/%s' % (settings.MEDIA_ROOT, self.id)

        if os.path.exists(dir):
            shutil.rmtree(dir)

    owner = models.ForeignKey(User, verbose_name=u"Usuário", on_delete=models.CASCADE)

    type = models.CharField(u'Carousel', max_length=50,
                            choices=carousel_choices)
    published = models.BooleanField(u'Publicado', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    carousel_order = models.PositiveIntegerField(default=0, editable=False,
                                                 db_index=True)

    u''' Managers '''
    objects = models.Manager()
    activated = CarouselActivatedManager()

    def images_set(self):
        photo = self.photo_set.order_by('photo_order')
        return photo
