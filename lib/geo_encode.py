from geopy.geocoders import Nominatim


def address_to_geopoint(address):

    geolocator = Nominatim(user_agent="SmartMeet")
    location = geolocator.geocode(address)

    return location.latitude, location.longitude