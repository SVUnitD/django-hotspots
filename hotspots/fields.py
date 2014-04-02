from django.db import models
from .widgets import HotspotWidget


class HotspotField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.image_field = kwargs.pop('image_field')
        kwargs['blank'] = True
        kwargs['max_length'] = 255
        super(HotspotField, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = HotspotWidget(self.image_field)
        return super(HotspotField, self).formfield(*args, **kwargs)

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        """
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
