from django import forms
from django.utils.safestring import mark_safe


class HotspotWidget(forms.TextInput):
    def __init__(self, image_field, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['data-image_field'] = image_field
        super(HotspotWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        html = [super(HotspotWidget, self).render(name, value, attrs)]
        final_attrs = self.build_attrs(attrs)
        pos = final_attrs['id'].find('__prefix__')
        if pos != -1:
            html.append('''<script type="text/javascript">
setTimeout(function () {
    var id = '%s';

    if (typeof(window._hotspots_inited) == 'undefined') {
        window._hotspots_inited = true;
    } else {
        var elements = id.replace(/__prefix__/, parseInt(document.getElementById('%sTOTAL_FORMS').value) - 1);
        if (document.getElementById(elements)) {
            Hotspot.init(elements);
        }
    }
}, 0);
</script>''' % (final_attrs['id'], final_attrs['id'][0:pos]))
        else:
            html.append('<script type="text/javascript">Hotspot.init("%s");</script>''' % (final_attrs['id']))
        return mark_safe(u'\n'.join(html))

    class Media:
        js = ("hotspots/js/hotspots.js",)
        css = {'all': ("hotspots/css/hotspots.css",)}
