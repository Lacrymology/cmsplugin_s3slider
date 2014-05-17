from cms.utils import cms_static_url
from inline_ordering.admin import OrderableStackedInline, INLINE_ORDERING_JS
import forms
import models


class ImageInline(OrderableStackedInline):

    model = models.Image

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            kwargs.pop('request', None)
            kwargs['widget'] = forms.AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageInline, self).\
            formfield_for_dbfield(db_field, **kwargs)

    @property
    def media(self):
        js = [cms_static_url(path) for path in (
            'js/libs/jquery.ui.core.js',
            'js/libs/jquery.ui.sortable.js',
            )]
        media = super(ImageInline, self).media
        if js[-1] not in media._js:
            ix = media._js.index(INLINE_ORDERING_JS)
            media._js[ix:ix] = js
        return media
