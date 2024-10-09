import overpass
import geojson

api = overpass.API(timeout=500)

def grab_osm_data(query, name):
    # api.get already returns a FeatureCollection, a GeoJSON type
    res = api.get(query, verbosity='geom')
    # if you want a str, then use dumps function
    #geojson_str = geojson.dumps(res)
    # for feature in res['features']:
    #     feature['properties']['id'] = feature['id']

    # dump as file, if you want to save it in file
    with open(f"./geo_data/{name}.geojson",mode="w") as f:
        geojson.dump(res,f)

    # node_ids = [feature['id'] for feature in res['features']]



if __name__ == '__main__':

    box = "46.8410025,-123.2330404,48.2494561,-121.6019589"

    query = f"""
        (
        node["amenity"]({box});
        );
    """

    grab_osm_data(query, 'amenity')

    query = f"""
        (
        node["shop"]({box});
        );
    """

    grab_osm_data(query, 'shop')

