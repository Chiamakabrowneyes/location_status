from shapely.geometry import Polygon, MultiPolygon, mapping
from status import in_bounds_geojson

def test_simple_square_inside():
    square = Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])
    assert in_bounds_geojson(mapping(square), (0.5, 0.5)) is True

def test_simple_square_outside():
    square = Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])
    assert in_bounds_geojson(mapping(square), (2.0, 2.0)) is False

def test_boundary_counts_as_in():
    square = Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])
    assert in_bounds_geojson(mapping(square), (1.0, 0.5)) is True

def test_concave_polygon_inside_hollow():
    concave = Polygon([(0,0),(0,4),(1,4),(1,1),(3,1),(3,0),(0,0)])
    assert in_bounds_geojson(mapping(concave), (0.5, 0.5)) is True

def test_polygon_with_hole_out_in_hole():
    outer = [(0,0),(0,4),(4,4),(4,0),(0,0)]
    hole  = [(1,1),(1,3),(3,3),(3,1),(1,1)]
    donut = Polygon(outer, [hole])
    assert in_bounds_geojson(mapping(donut), (2.0, 2.0)) is False
    assert in_bounds_geojson(mapping(donut), (0.5, 0.5)) is True

def test_multipolygon():
    a = Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])
    b = Polygon([(3,3),(3,4),(4,4),(4,3),(3,3)])
    mp = MultiPolygon([a, b])

    assert in_bounds_geojson(mapping(mp), (0.5, 0.5)) is True
    assert in_bounds_geojson(mapping(mp), (3.5, 3.5)) is True
    assert in_bounds_geojson(mapping(mp), (2.0, 2.0)) is False

