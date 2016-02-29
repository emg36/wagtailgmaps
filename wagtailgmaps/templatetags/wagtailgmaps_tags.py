import uuid

from django import template
from django.conf import settings

from distutils.version import StrictVersion

from wagtailgmaps.utils import get_wagtail_version

register = template.Library()


# Map template
@register.inclusion_tag('wagtailgmaps/map_editor.html')
def map_editor(address, width, width_units, height, height_units, zoom=None):
    """
    Tag to output a Google Map with the given attributes
    """
    if (address is None) or (address == ""):
        address = settings.WAGTAIL_ADDRESS_MAP_CENTER

    map_id = uuid.uuid4()  # Something a bit simpler would be probably ok too..

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

    for s in self.children:
        if s.id_for_label() == 'id_start_address':
            start_address = s.bound_field.value()
        if s.id_for_label() == 'id_end_address':
            end_address = s.bound_field.value()

    if (start_address is None) or (start_address == ""):
        start_address = settings.WAGTAIL_DIRECTIONS_START_ADDRESS

    if (end_address is None) or (end_address == ""):
        end_address = settings.WAGTAIL_DIRECTIONS_END_ADDRESS

    if (travel_mode is None) or (travel_mode == ""):
        travel_mode = 'DRIVING'

    map_id = uuid.uuid4()  # Something a bit simpler would be probably ok too..

    return {
        'map_id': map_id,
        'start_address': start_address,
        'end_address': end_address,
        'travel_mode': travel_mode,
        'width': width,
        'width_units': width_units,
        'height': height,
        'height_units': height_units,
    }


@register.inclusion_tag('wagtailgmaps/api_key.html')
def api_key():
    """
    Return a string version of the google maps api kei from settings
    """

    return {
        'api_key': settings.WAGTAIL_GOOGLE_MAPS_API_KEY
    }
