wagtailgmaps
==================

A fork from sprinload/wagtailgmaps with some changes purely for my benefit in a particular project. Some minor changes to add a lat/lng input as well as the actual address. 

I have the default address for the map as 'Christchurch, New Zealand'. If you change this you might want to change the condition in the js looking comparing the params.address.

Call the tag with the map_geo i.e. latlng rather than an address to set the marker where you want rather than setting the marker in the default position within the address. {% map_editor form.map_geo.value 100 "%" 300 "px" 16 %}

![Wagtailgmaps screenshot](http://i.imgur.com/9m9Gfcf.png)

Simple Google Maps address formatter for Wagtail fields.

# Quickstart

Assuming you have a [Wagtail](https://wagtail.io/) project up and running:

``` $ pip install git+https://github.com/emg36/wagtailgmaps.git ```

add wagtailgmaps to your `settings.py` in the INSTALLED_APPS section before!!! wagtail.wagtailadmin:

```
...
    'wagtailgmaps',
...
    'wagtail.wagtailadmin',
...
```

Add a couple of necessary constants in your `settings.py` file:

```
...
WAGTAIL_ADDRESS_MAP_CENTER = 'Wellington, New Zealand'
WAGTAIL_ADDRESS_MAP_ZOOM = 8
...
```
`WAGTAIL_ADDRESS_MAP_CENTER` must be a properly formatted address. Also, remember valid zoom levels go from 0 to 18. See [Map options](https://developers.google.com/maps/documentation/javascript/tutorial#MapOptions) for details.

As for now, only fields using `FieldPanel` inside a `MultiFieldPanel` are supported. This is due to the lack of support of the `classname` attribute for other panel fields other than `MultiFieldPanel`.

In your `models.py`, your custom Page model would have something similar to:

```
map_address = models.CharField('Map address', max_length=255)
map_geo = models.CharField('Map geolocation', max_length=255)
...    
    
MultiFieldPanel([
        FieldPanel('map_address'),
        FieldPanel('map_geo', classname="gmap"),
    ], heading="Address")
```

Notice the `FieldPanel` is embedded in a `MultiFieldPanel`, even if it only contains a single element. If you define your `FieldPanel` outside it won't work. The app supports more than one map (field) at the same time.

The classname goes on the second panel as the javascript fills it's first parent input field with the lat/lng and the input field previous to that with the address field.

When editing the model from the admin interface the affected field shows up with a map, like the screenshot above.

The field gets updated according to the [Google Geocoding Service](https://developers.google.com/maps/documentation/geocoding/) each time:

* The map market gets dragged and dropped into a location (`dragend` JS event).
* Click happens somewhere in the map (`click` JS event).
* Return key is pressed after editing the field (`enterKey` JS event for return key only).

Feel free to edit the provided JS to add/edit the events you might need.

Once your address field is properly formatted and stored in the database you can use it in your front end Django templates. Example:

```
<a href="http://maps.google.com/?q={{ map_address }}">Open map</a>
```
