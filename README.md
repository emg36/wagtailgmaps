wagtailgmaps
==================

A fork from springload/wagtailgmaps with some changes purely for my benefit in a particular project. Some minor changes to add a lat/lng input as well as the actual address. 

I have the default address for the map as 'Christchurch, New Zealand'. If you change this you might want to change the condition in the js looking comparing the params.address.

Call the tag with the map_geo i.e. latlng rather than an address to set the marker where you want rather than setting the marker in the default position within the address. {% map_editor form.map_geo.value 100 "%" 300 "px" 16 %}

![Imgur](http://i.imgur.com/4QQ5dub.png)

![Imgur](http://i.imgur.com/LYpOoe5.png)


Simple Google Maps address formatter for Wagtail fields.

# Quickstart

This module only supported in Django 1.9+ and Wagtail 2.0+

Assuming you have a [Wagtail](https://wagtail.io/) project up and running:

``` $ pip install git+https://github.com/emg36/wagtailgmaps.git ```

add wagtailgmaps to your `settings.py` in the INSTALLED_APPS section **before** wagtail.admin:

```
INSTALLED_APPS = [
...
    'wagtailgmaps',
...
    'wagtail.admin',
...
]
```

Add a couple of necessary constants in your `settings.py` file, these are used as initial default values:

```
...
WAGTAIL_ADDRESS_MAP_CENTER = 'Wellington, New Zealand'
WAGTAIL_ADDRESS_MAP_ZOOM = 8

WAGTAIL_DIRECTIONS_START_ADDRESS = 'Christchurch, New Zealand'
WAGTAIL_DIRECTIONS_END_ADDRESS = 'Greymouth, New Zealand'
WAGTAIL_GOOGLE_MAPS_API_KEY = '***'
```

Don't forget to add these into the googles developers console and enable the correct api's (javascript, geocoding, directions, geolocation)
...

`WAGTAIL_ADDRESS_MAP_CENTER` must be a properly formatted address. Also, remember valid zoom levels go from 0 to 18. See [Map options](https://developers.google.com/maps/documentation/javascript/tutorial#MapOptions) for details.

`FieldPanel` and `InlinePanel` inside a `MultiFieldPanel` are supported.

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

if using an inline solution (like an Orderable), the panels should be set up like so:
```
class Address(Orderable):
    page = ParentalKey('app.AddressDirectoryPage, related_name='address_related', on_delete=models.CASCADE)
    map_address = CharField('Map address', max_length=255)
    map_geo = CharField('Map geolocation', max_length=255)
    
    panels = [
        FieldPanel('map_address'),
        FieldPanel('map_geo'),
    ]

class AddressDirectoryPage(Page):
    ...

AddressDirectoryPage.content_panels = [
    ...
    MultiFieldPanel([
        InlinePanel('address_related'),
    ], heading='Many addresses),
    ...
]
```

for directions use the following:
```
start_place = models.CharField('Starting place', max_length=255, help_text='e.g. Christchurch, NZ. Click in text field and press the update button to set map')
end_place = models.CharField('End place', max_length=255, help_text='e.g. Greymouth, NZ. Click in text field and press the update button to set map')

travel_choices = (
    ("DRIVING","DRIVING"),
    ("TRANSIT","TRANSIT"),
    ("WALKING","WALKING"),
)
travel_mode = models.CharField('Travel mode', choices=travel_choices, max_length=30, default='DRIVING')
distance = models.CharField('Distance', max_length=40, help_text='Display only')
travel_time = models.CharField("Travel time", max_length=40, help_text='Display only')
...

MultiFieldPanel([
      FieldPanel('distance', classname=''),
      FieldPanel('travel_time', classname=''),
      FieldPanel('travel_mode'),
      FieldPanel('start_place'),
      FieldPanel('end_place', classname='gmap_directions'),
], heading='Travel times', classname='collapsible gmap_directions_holder'),
        
```

Notice the `FieldPanel` is embedded in a `MultiFieldPanel`, even if it only contains a single element. If you define your `FieldPanel` outside it won't work. The app supports more than one map (field) at the same time.
EXCEPT in the above mentioned case where an 'inline solution' is being used.

The classname goes on the second panel as the javascript fills it's first parent input field with the lat/lng and the input field previous to that with the address field.

When editing the model from the admin interface the affected field shows up with a map, like the screenshot above.

The field gets updated according to the [Google Geocoding Service](https://developers.google.com/maps/documentation/geocoding/) each time:

* The map market gets dragged and dropped into a location (`dragend` JS event).
* Click happens somewhere in the map (`click` JS event).
* 'Update Map' is clicked after editing the field (`click` JS event).

Feel free to edit the provided JS to add/edit the events you might need.

Once your address field is properly formatted and stored in the database you can use it in your front end Django templates. Example:

```
<a href="http://maps.google.com/?q={{ map_address }}&key={% api_key %}">Open map</a>
```


To set the coordinates field to readonly, add the following widget when defining your FieldPanel:
```
...
MultiFieldPanel([
    FieldPanel('map_address'),
    FieldPanel('map_geo', classname='gmap', widget=TextInput(attrs={'readonly':'readonly'}))
], heading='Address')
```

Similarly to hide the coordinates field:
```
...
    FieldPanel('map_geo', classname='gmap', widget=TextInput(attrs={'hidden':'hidden'}))
...
```

For using the map in the front end, the following template tag must be loaded and given parameters for this function:
```
def map_editor(self, width, width_units, height, height_units, zoom=None, front_end=False):
...
```
So the code in the template should look like this:
```
{% map_editor map_geo width=100 width_units="%" height=50 height_units="%" zoom=None front_end="True" %}
```
The use case for this is to open up a frontend form that uses the map fields.
