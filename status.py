from constants import *
import requests
from shapely.geometry import Point, shape

"""Returns the parameter bounds and checks if the point is within bounds"""
def in_bounds_geojson(zone, point):
    poly = shape(zone)
    lon, lat = point
    return poly.covers(Point(lon, lat))

"""Returns the points and polygon for each clinician. """
def get_clinician_status(clinician_id):
    data = requests.get(f"{API_URL}/{clinician_id}").json()
    if not data:
        return None
    point = None
    zone = None

    for feature in data['features']:
        if feature['geometry']['type'] == 'Point':
            point = feature['geometry']['coordinates']
        elif feature['geometry']['type'] in {"Polygon", "MultiPolygon"}:
            zone = feature['geometry']
    if not point or not zone:
        return None
    return in_bounds_geojson(zone, point)


"""Returns status for all clinicians"""
def check_clinician_in_bounds():
    result_status = []
    for clinician in CLINICIAN_LIST:
        result_status.append(get_clinician_status(clinician))
    return result_status

print(check_clinician_in_bounds())










