import logging
from django.http import Http404
from django.conf import settings
from django.template import RequestContext
from django.conf.urls import patterns, url
from django.db.models.fields.files import ImageFieldFile
from django.shortcuts import get_object_or_404, render_to_response

from easy_thumbnails.files import get_thumbnailer

logger = logging.getLogger(__name__)


class HotspotAdminMixin(object):
    def get_urls(self):
        urls = patterns(
            '',
            url(r'^(\d+)/hotspot_thumbnail/$',
                self.admin_site.admin_view(self.hotspot_thumbnail))
        )
        return urls + super(HotspotAdminMixin, self).get_urls()

    def hotspot_thumbnail(self, request, instance_pk):
        thumb = error = None
        image_field = request.GET['image_field']
        instance_pk = int(instance_pk)
        instance = get_object_or_404(self.model, pk=instance_pk)

        if bool(request.GET.get('inline', u'false')):
            # strip off first fk
            _, image_field = image_field.split('__', 1)

        field = instance
        try:
            for field_name in image_field.split('__'):
                if field:
                    field = getattr(field, field_name)

                if field is None:
                    error = u'Please set an image (%s) in %s.' % (
                        image_field, self.model)
                    break

        except AttributeError:
            logger.error("Could not resolve ImageField %s for %s(pk=%d)." % (
                image_field, unicode(self.model), instance_pk))
            raise Http404()

        if field:
            if not isinstance(field, ImageFieldFile):
                logger.error("%s is not an ImageField." % (image_field))
                raise Http404()

            thumbnailer = get_thumbnailer(field)
            thumbnail_options = {
                'detail': True,
                'size': getattr(settings, 'HOTSPOT_THUMB_SIZE', (300, 300)),
            }
            thumb = thumbnailer.get_thumbnail(thumbnail_options)

        return render_to_response(
            'hotspots/thumbnail.html',
            {
                'thumbnail': thumb,
                'error': error,
            },
            context_instance=RequestContext(request)
        )
