from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from sorl.thumbnail import ImageField
from django_extensions.db.fields import AutoSlugField

class GalleryBase(TimeStampedModel):
    image = ImageField(upload_to='uploaded', null=True, blank=True)
    is_published = models.BooleanField(_("is published"), default=False)
    video_link = models.URLField(_('video_link'), null=True, blank=True)
    image_link = models.URLField(_('image_link'), null=True, blank=True)
    # django_extensions AutoSlugField is sucks.
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    slug = models.SlugField(_('slug'), null=True, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)
    ordering = models.IntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return self.title

    def get_image_url(self):
        return self.image_link or self.video_link or self.image.url

    def preview(self):
        url = self.image_link or (self.image and self.image.url)
        return url and '<img src="%(url)s" width="%(width)spx">' % dict(url=url, width=140) or ""
    preview.allow_tags = True
    
    class Meta:
        abstract = True
        ordering = ('ordering',)

GALLERY_DISPLAY_TYPES = (
    (1, '1 column'),
    (2, '2 columns'),
    (3, '3 columns'),
    (4, '4 columns'),
)

class Gallery(GalleryBase):
    display_type = models.IntegerField(choices=GALLERY_DISPLAY_TYPES, default=1)

    @models.permalink
    def get_absolute_url(self):
        return ('galleria', (), {'slug': self.slug})

    class Meta:
        verbose_name_plural=_("Galleries")

class Photo(GalleryBase):
    gallery = models.ForeignKey(Gallery, related_name='photos', null=True, blank=True)

    def get_absolute_url(self):
        return self.get_image_url()

    class Meta:
        verbose_name_plural=_("Photos")
