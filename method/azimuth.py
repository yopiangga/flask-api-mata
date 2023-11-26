import math

def calculate_azimuth(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    # Calculate the differences in longitude and latitude
    delta_lon = lon2 - lon1

    # Calculate the azimuth (direction) using the haversine formula
    y = math.sin(delta_lon)
    x = math.cos(lat1) * math.tan(lat2) - math.sin(lat1) * math.cos(delta_lon)
    azimuth = math.atan2(y, x)

    # Convert azimuth from radians to degrees
    azimuth = math.degrees(azimuth)

    # Normalize the azimuth to the range [0, 360] degrees
    azimuth = (azimuth + 360) % 360

    return azimuth