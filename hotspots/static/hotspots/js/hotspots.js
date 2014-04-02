var Hotspot = {
    init: function(id) {
        $ = django.jQuery;
        var $field = $('#'+id);

        var data = {
            'image_field': $field.attr('data-image_field'),
            'inline': (id.indexOf("set") > 0)
        };
        $.get('hotspot_thumbnail/', data, function(html) {
            var $hotspot_html = $(html);
            $field.hide();
            $hotspot_html.insertAfter($field);

            var $image_wrapper = $hotspot_html.find('.image-wrapper');
            if (!$image_wrapper) return;  // image not available

            var $img = $image_wrapper.find('img');
            var $marker = $image_wrapper.find('.marker');
            $marker.hide();

            // load initial position
            if ($field.val()) {
                $img.load(function() {
                    var pos = $field.val().split(',');
                    var x = parseFloat(pos[0]) * $img.width();
                    var y = parseFloat(pos[1]) * $img.height();
                    if (x != "NaN" && y != "NaN") {
                        $marker.css({'left': x, 'top': y});
                        $marker.show();
                    }
                });
            }

            $img.click(function(ev) {
                var offset = $(this).offset();
                var x = ev.pageX - offset.left - $marker.outerWidth()/2;
                var y = ev.pageY - offset.top - $marker.outerHeight()/2;

                $marker.css({'left': x, 'top': y});
                $marker.show();
                $field.val((x/$img.width()) + ',' + y/$img.height());
            });
        });
    }
}
