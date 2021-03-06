from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from sekizai.context import SekizaiContext

import admin
import models


class CMSGalleryPlugin(CMSPluginBase):

    model = models.GalleryPlugin
    inlines = [admin.ImageInline, ]
    name = _('Image gallery')
    render_template = 'cmsplugin_s3slider/gallery.html'

    def render(self, context, instance, placeholder):
        context.update({
                        'images': instance.images.all(),
                        'gallery': instance,
                        'slider_id': "slider%d"%instance.pk,
                       })
        self.render_template = instance.template
        return context


plugin_pool.register_plugin(CMSGalleryPlugin)
