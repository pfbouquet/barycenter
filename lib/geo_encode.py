from geopy.geocoders import Nominatim


def address_to_geopoint(address):

    geo_locator = Nominatim(user_agent="SmartMeet")
    location = geo_locator.geocode(address)

    return location.longitude, location.latitude
