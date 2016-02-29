$(document).ready(function() {

  google.maps.event.addDomListener(window, 'load', function() {

    // One geocoder var to rule them all
    var geocoder = new google.maps.Geocoder();

    // Get formatted address from LatLong position
    function geocodePosition(pos, input, input2) {
      geocoder.geocode({
        latLng: pos
      }, function(responses) {
        if (responses && responses.length > 0) {
            $(input).val(responses[0].formatted_address);
            $(input2).val(responses[0].geometry.location.lat() + ", " + responses[0].geometry.location.lng());
        } else {
          alert('Cannot determine address at this location.');
        }
      });
    }

    // Get LatLong position and formatted address from inaccurate address string
    function geocodeAddress(address, input, input2, marker, map) {
      geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          marker.setPosition(results[0].geometry.location);
          $(input).val(results[0].formatted_address);
          $(input2).val(results[0].geometry.location.lat() + ", " + results[0].geometry.location.lng());
          map.setCenter(results[0].geometry.location);
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        }
      });
    }

    function update_directions(mapElem, map, directionsService, directionsDisplay) {
      directionsService.route({
        origin: mapElem.start.val(),
        destination: mapElem.end.val(),
        travelMode: [
          google.maps.TravelMode[$('#id_travel_mode').val()],
        ],
        unitSystem: google.maps.UnitSystem.METRIC
      }, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
          mapElem.distance.val(response.routes[0].legs[0].distance.text);
          mapElem.travel_time.val(response.routes[0].legs[0].duration.text);
        } else {
          window.alert('Directions request failed due to ' + status);
        }
      });
    }

    function set_address(mapElem, latlng, mapId, map_key, zoom, map, marker){
      mapElem[map_key] = document.getElementById(mapId);
      // Usually the address input is the first input sibling of the map container..
      mapElem.input = $("#" + mapId).parent().prev().find("input:first");
      mapElem.input2 = $("#" + mapId).parent().find("input:first");
      // Create map options and map
      var mapOptions = {
          zoom: zoom,
          center: latlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };

      map[map_key] = new google.maps.Map(mapElem[map_key], mapOptions);
      marker[map_key] = new google.maps.Marker({
        position: latlng,
        map: map[map_key],
        draggable: true
      });
      // Set events listeners to update marker/input values/positions
      google.maps.event.addListener(marker[map_key], 'dragend', function(event) {
        geocodePosition(marker[map_key].getPosition(), mapElem.input, mapElem.input2);
      });
      google.maps.event.addListener(map[map_key], 'click', function(event) {
        marker[map_key].setPosition(event.latLng);
        geocodePosition(marker[map_key].getPosition(), mapElem.input, mapElem.input2);
      });

      // Event listeners to update map when press enter or tab
      $(mapElem.input).bind("enterKey",function(event) {
        geocodeAddress($(this).val(), mapElem.input, mapElem.input2, marker[map_key], map[map_key]);
      });
      $(mapElem.input2).bind("enterKey",function(event) {
        geocodeAddress($(this).val(), mapElem.input, mapElem.input2, marker[map_key], map[map_key]);
      });

      $(mapElem.input).keypress(function(event) {
          if(event.keyCode == 13)
          {
            event.preventDefault();
            $(this).trigger("enterKey");
          }
      });
      $(mapElem.input2).keypress(function(event) {
          if(event.keyCode == 13)
          {
            event.preventDefault();
            $(this).trigger("enterKey");
          }
      });
    }

    function set_directions(mapElem, mapId, map_key, map, travel_mode, directionsService, directionsDisplay) {
      mapElem[map_key] = document.getElementById(mapId);
      // Usually the address input is the first input sibling of the map container..
      mapElem.start = $("#id_start_place");
      mapElem.end = $("#id_end_place");
      mapElem.travel_mode = $('#id_travel_mode');
      mapElem.distance = $('#id_distance');
      mapElem.travel_time = $('#id_travel_time');

      mapElem.distance.attr('readonly', true);
      mapElem.travel_time.attr('readonly', true);

      var styles = [
        {
          "featureType": "administrative",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "poi",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "landscape",
          "stylers": [
            { "visibility": "simplified" },
            { "hue": "#00ff5e" },
            { "saturation": 20 },
            { "lightness": 20 }
          ]
        },{
          "featureType": "road.arterial",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "road.local",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "water",
          "elementType": "labels",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "landscape",
          "elementType": "labels",
          "stylers": [
            { "visibility": "off" }
          ]
        },{
          "featureType": "administrative.locality",
          "stylers": [
            { "visibility": "on" }
          ]
        },{
          "featureType": "water",
          "stylers": [
            { "hue": "#0091ff" }
          ]
        },{
        }
      ]
      // Create map options and map
      var mapOptions = {
          // zoom: zoom,
          // center: latlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          styles: styles,
      };

      if (mapElem.start.val() != '') {
        directionsService.route({
          origin: mapElem.start.val(),
          destination: mapElem.end.val(),
          travelMode: google.maps.TravelMode.DRIVING
        }, function(response, status) {
          if (status === google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
            mapElem.distance.val(response.routes[0].legs[0].distance.text);
            mapElem.travel_time.val(response.routes[0].legs[0].duration.text);
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      };

      map[map_key] = new google.maps.Map(mapElem[map_key], mapOptions);
      directionsDisplay.setMap(map[map_key]);
      // Event listeners to update map when press enter or tab
      $(mapElem.start).bind("enterKey",function(event) {
        update_directions(mapElem, map, directionsService, directionsDisplay);
      });
      $(mapElem.end).bind("enterKey",function(event) {
        update_directions(mapElem, map, directionsService, directionsDisplay);
      });
      $(mapElem.travel_mode).on("change",function(event) {
        update_directions(mapElem, map, directionsService, directionsDisplay);
      });

      $(mapElem.start).keypress(function(event) {
          if(event.keyCode == 13)
          {
            event.preventDefault();
            $(this).trigger("enterKey");
          }
      });
      $(mapElem.end).keypress(function(event) {
          if(event.keyCode == 13)
          {
            event.preventDefault();
            $(this).trigger("enterKey");
          }
      });
      // $(mapElem.travel).keypress(function(event) {
      //     if(event.keyCode == 13)
      //     {
      //       event.preventDefault();
      //       $(this).trigger("enterKey");
      //     }
      // });
    }


    // Method to initialize a map and all of its related components (usually address input and marker)
    window.initialize_map = function (params) {

      // Get latlong form address to initialize map
      geocoder.geocode( { "address": params.address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          if (params.address != 'Christchurch, New Zealand') {
              var geo_dict = new google.maps.LatLng(parseFloat(params.address.split(', ')[0]), parseFloat(params.address.split(', ')[1]));
          } else {
              geo_dict = results[0].geometry.location;
          };
          set_address({}, results[0].geometry.location, "map-canvas-" + params.map_id, params.map_id, params.zoom, {}, {});
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        };
      });

    }

    window.initialize_map_directions = function (params) {
      var directionsService = new google.maps.DirectionsService;
      var directionsDisplay = new google.maps.DirectionsRenderer({suppressMarkers: true});

      // Get latlong from start and end to initialize directions map
      var start_address, end_address;
      geocoder.geocode( {'address': params.start_address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          start_address = results[0].geometry.location
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        };
      });
      geocoder.geocode( {'address': params.end_address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          end_address = results[0].geometry.location
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        };
      });
      set_directions({}, "map-canvas-" + params.map_id, params.map_id, {}, params.travel_mode, directionsService, directionsDisplay);
    }

    // Trigger the event so the maps can start doing their things
    var event; // The custom event that will be created

    if (document.createEvent) {
      event = document.createEvent("HTMLEvents");
      event.initEvent("wagtailmaps_ready", true, true);
    } else {
      event = document.createEventObject();
      event.eventType = "wagtailmaps_ready";
    }

    event.eventName = "wagtailmaps_ready";

    if (document.createEvent) {
      document.dispatchEvent(event);
    } else {
      document.fireEvent("on" + event.eventType, event);
    }

  });

});
