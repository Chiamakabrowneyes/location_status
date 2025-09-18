from shapely.geometry import Point, MultiPoint
from constants import *
import requests


"""Returns the parameter bounds and checks if the point is within bounds"""
def in_bounds_shapely(points, p):
    hull = MultiPoint(points).convex_hull
    return hull.covers(Point(p))


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
            zone = feature['geometry']['coordinates'][0]
    if not point or not zone:
        return None
    return in_bounds_shapely(zone, point)


"""Returns status for all clinicians"""
def check_clinician_in_bounds():
    result_status = []
    for clinician in CLINICIAN_LIST:
        result_status.append(get_clinician_status(clinician))
    return result_status

print(check_clinician_in_bounds())










