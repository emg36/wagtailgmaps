import uuid

from django import template
from django.conf import settings

from distutils.version import StrictVersion

from wagtailgmaps.utils import get_wagtail_version

register = template.Library()


# Map template
@register.inclusion_tag('wagtailgmaps/map_editor.html')
def map_editor(self, width, width_units, height, height_units, zoom=None):
    """
    Tag to output a Google Map with the given attributes
    """
    address = self.children[0].bound_field.value
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
    # print(self.__dict__)
    for s in self.children:
        # print(s.bound_field.__dict__) #, s.id_for_label(), s.__dict__)
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
        # print(s.bound_field.__dict__)
        # print(s.instance.__dict__, self.instance.__dict__)

    if (start_address is None) or (start_address == ""):
        start_address = settings.WAGTAIL_DIRECTIONS_START_ADDRESS

    if (end_address is None) or (end_address == ""):
        end_address = settings.WAGTAIL_DIRECTIONS_END_ADDRESS

    if (travel_mode is None) or (travel_mode == ""):
        travel_mode = 'DRIVING'

    # map_id = uuid.uuid4()  # Something a bit simpler would be probably ok too..
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


@register.inclusion_tag('wagtailgmaps/api_key.html')
def api_key():
    """
    Return a string version of the google maps api kei from settings
    """

    return {
        'api_key': settings.WAGTAIL_GOOGLE_MAPS_API_KEY
    }
