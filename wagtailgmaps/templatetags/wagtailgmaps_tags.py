from django import template
from django.conf import settings

register = template.Library()


# Map template
@register.inclusion_tag('wagtailgmaps/map_editor.html')
def map_editor(self, width, width_units, height, height_units, zoom=None, front_end=False):
    """
    Tag to output a Google Map with the given attributes
    """

    if (self is None) or (self == ""): # this is for an outlier that might be a frontend map but want the map to render rather than error
        address = settings.WAGTAIL_ADDRESS_MAP_CENTER
    elif front_end == 'True':
        address = self
    else:
        # backend map that isn't inline and inside a multifield
        address = self.children[0].bound_field.value()
        if (address is None) or (address == ""):
            address = settings.WAGTAIL_ADDRESS_MAP_CENTER
        for s in self.children:
            if s.bound_field.name == 'map_address':
                address = s.bound_field.value()
                if (address is None) or (address == ""):
                    address = settings.WAGTAIL_ADDRESS_MAP_CENTER
    try:
        if self.instance.sort_order:
            map_id = 'id_maptest-{0}'.format(self.instance.sort_order)
        else:
            map_id = 'id_maptest-__prefix__'
    except Exception:
        # this needs to have unique map id per instance/multi field.
        # Use case is when multi inline panels are created but the page doesn't 
        # save correctly and the unique orderable id's are thrown out the window
        try:
            if 'children' in self.__dict__.keys():
                map_id = 'id_map-{0}'.format(self.children[0].field_name)
        except Exception:
            map_id = 'id_maptest-only'

    if zoom is None:
        zoom = settings.WAGTAIL_ADDRESS_MAP_ZOOM

    return {
        'map_id': map_id,
        'address': address,
        'zoom': zoom,
        'width': width,
        'width_units': width_units,
        'height': height,
        'height_units': height_units,
    }
    

# Map directions template
@register.inclusion_tag('wagtailgmaps/map_editor_directions.html')
def map_editor_directions(self, width, width_units, height, height_units):
    """
    Tag to output a Google Map with the given attributes
    """

    start_address = None
    end_address = None
    travel_mode = None
    start_address_id = 'id_start_address'
    end_address_id = 'id_end_address'
    travel_mode_id = 'id_travel_mode'
    distance_id = 'id_distance'
    time_id = 'id_travel_time'
    for s in self.children:
        if s.bound_field.name == 'start_place': #id_for_label() == 'id_start_address':
            start_address = s.bound_field.value()
            start_address_id = s.bound_field.id_for_label
        if s.bound_field.name == 'end_place': #id_for_label() == 'id_end_address':
            end_address = s.bound_field.value()
            end_address_id = s.bound_field.id_for_label
        if s.bound_field.name == 'travel_mode': #id_for_label() == 'id_end_address':
            travel_mode = s.bound_field.value()
            travel_mode_id = s.bound_field.id_for_label
        if s.bound_field.name == 'distance': #id_for_label() == 'id_end_address':
            distance = s.bound_field.value()
            distance_id = s.bound_field.id_for_label
        if s.bound_field.name == 'travel_time': #id_for_label() == 'id_end_address':
            travel_time = s.bound_field.value()
            travel_time_id = s.bound_field.id_for_label

    if (start_address is None) or (start_address == ""):
        start_address = settings.WAGTAIL_DIRECTIONS_START_ADDRESS

    if (end_address is None) or (end_address == ""):
        end_address = settings.WAGTAIL_DIRECTIONS_END_ADDRESS

    if (travel_mode is None) or (travel_mode == ""):
        travel_mode = 'DRIVING'

    try:
        if self.instance.sort_order:
            map_id = 'id_day-{0}'.format(self.instance.sort_order)
        else:
            map_id = 'id_day-__prefix__'
    except Exception:
        map_id = 'id_day-only'

    return {
        'map_id': map_id,
        'start_address': start_address,
        'end_address': end_address,
        'travel_mode': travel_mode,
        'width': width,
        'width_units': width_units,
        'height': height,
        'height_units': height_units,
        'start_address_id': start_address_id,
        'end_address_id': end_address_id,
        'travel_mode_id': travel_mode_id,
        'distance_id': distance_id,
        'time_id': travel_time_id,
    }


@register.simple_tag
def api_key():
    """
    Return a string version of the google maps api key from settings
    """

    return settings.WAGTAIL_GOOGLE_MAPS_API_KEY
    
