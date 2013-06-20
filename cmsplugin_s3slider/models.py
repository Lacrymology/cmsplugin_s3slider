import threading
from django.core.exceptions import ValidationError

from cms.models import CMSPlugin, Page
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from inline_ordering.models import Orderable

import utils

localdata = threading.local()
localdata.TEMPLATE_CHOICES = utils.autodiscover_templates()
TEMPLATE_CHOICES = localdata.TEMPLATE_CHOICES

class GalleryPlugin(CMSPlugin):

    template = models.CharField(
        max_length=255,
        choices=TEMPLATE_CHOICES,
        default='cmsplugin_s3slider/gallery.html',
        editable=len(TEMPLATE_CHOICES) > 1)

    timeout = models.IntegerField(default=3000)
    
    POSITIONS = (
        ('left', _('Left')),
        ('right', _('Right')),
        ('center', _('Center')),
        )
    alignment = models.CharField(max_length=8,
                                 choices=POSITIONS,
                                 default='left')
    
    def width(self):
        return max([i.src_width for i in self.images.all()])
    def height(self):
        return max([i.src_height for i in self.images.all()])

    def copy_relations(self, old_instance):
        for image in old_instance.images.all():
            image.pk = None
            image.gallery = self
            image.save()

    def __unicode__(self):
        return _(u'%(count)d image(s) in gallery') % {
            'count': self.images.count()
            }


class Image(Orderable):
    def get_media_path(self, filename):
        return self.gallery.get_media_path(filename)

    gallery = models.ForeignKey(GalleryPlugin, related_name='images')
    image = models.ImageField(upload_to=get_media_path,
                              height_field='src_height',
                              width_field='src_width', blank=True, null=True,
                              help_text=_("If this isn't filled, the image "
                                          "will fall back to 'image_url'"))
    image_url = models.CharField(max_length=128, blank=True, null=True,
                                 help_text=_(
                                     'If an image file is not uploaded, the '
                                     'image will fall back to this. '
                                     'Recommended for placeholders. Try '
                                     '"http://placekitten.com[/g]/'
                                     '(width)/(height)/"'))

    url = models.CharField(_("link"), max_length=255, blank=True, null=True,
                           help_text=_("if present image will be clickable"))
    page_link = models.ForeignKey(Page, verbose_name=_("page"), null=True,
                                  blank=True, help_text=_("if present, image "
                                                          "will be clickable"))

    src_height = models.PositiveSmallIntegerField(editable=False, null=True)
    src_width = models.PositiveSmallIntegerField(editable=False, null=True)
    alt = models.CharField(
        max_length=127,
        blank=True,
        )

    position_options = (
        ('top', _('Top')),
        ('bottom', _('Bottom')),
        ('left', _('Left')),
        ('right', _('Right')),
        )
    textPosition = models.CharField(
        default = 'bottom',
        choices = position_options,
        max_length = max([len(v) for (k,v) in position_options]),
        )
    title = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=2047, blank=True)

    def link(self):
        if self.page_link:
            lang = get_language()
            return self.page_link.get_absolute_url(language=lang)
        elif self.url:
            return self.url
        else:
            return "#"

    def clean(self):
        """
        Make sure either image or image_url are set
        """
        if not self.image and not self.image_url:
            raise ValidationError(_("At least one of image or image_url must "
                                    "be set."))
        return super(Image, self).clean()

    def url(self):
        """
        Return image_url if image doesn't exist
        """
        if self.image:
            return self.image.url
        return self.image_url

    def __unicode__(self):
        return self.title or self.alt or str(self.pk)
