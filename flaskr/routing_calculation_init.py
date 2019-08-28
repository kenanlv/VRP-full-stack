import json
import urllib.request
from app import User
import os


"""
Args:
   dis_mx: A 2D array, a, where a[i][j] represents from i to j distance
   capacities: A list, l, of integer where l[i] is the capacity of vehicle i
   origins: A list, l, of integer where l[i] is the index of starting location for vehicle i
   destination: A integer representing the index of the destination location
"""


def calculation_prepare():
    capacities = []
    origins = []
    locations = []
    locations_text = []
    email_list = []
    phone_num = []
    user_name = []
    all_users = User.query.all()  # for locations matrix
    i = 0
    for user in all_users:
        if getattr(user, 'is_driver'):
            capacities.append(getattr(user, 'capacity'))
            origins.append(i)
        # locations.append(getattr(user, 'address_show_txt')[:-5])
        locations.append(getattr(user, 'address_id'))
        locations_text.append(getattr(user, 'address_show_txt'))
        email_list.append(getattr(user, 'email'))
        phone_num.append(getattr(user, 'phone_number'))
        user_name.append(getattr(user, 'name'))
        i += 1

    # Convert locations
    # def get_distance(self):
    # Google MapsDdirections API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    # api_key = 'AIzaSyCLNO5mol_LjqDuOkTKLBke4Q9de-6GVy4'  # key from the internet
    api_key_distance_matrix = os.getenv('API_KEY_DIS')  # my api key do not share!!
    # Generate origins and destinations
    # origin = locations[0].replace(',', '')
    # origin = origin.replace(' ', '+')
    # origin = 'Toronto'
    starts = []
    for k in range(0, len(locations)):
        starts.append('place_id:' + locations[k])
    # origin = 'place_id:ChIJyX0Fy0sVkFQRJi5l_-c6fdw'
    # print(starts)
    # origin = input('Where are you?: ').replace(' ', '+')
    # destination = locations[1].replace(',', '')
    # destination = destination.replace(' ', '+')
    # destination = 'Montreal'
    # ends = ['place_id:' + locations[-1]]
    ends = 'place_id:' + locations[0]
    for j in range(1, len(locations)):
        ends += '|place_id:' + locations[j]
    destination = 'ChIJ6zWFnZIUkFQRoyu4AXksdGs|place_id=ChIJscQF-bNqkFQRqrFa919Xv5Y'
    # print(ends)
    dis_mx = []
    time_cost = []
    # print(dis_mx)
    for w in starts:
        # Building the URL for the request
        nav_request = 'origins={}&destinations={}&key={}'.format(w, ends, api_key_distance_matrix)
        request = endpoint + nav_request
        print(request)
        # Sends the request and reads the response.
        response = urllib.request.urlopen(request).read()
        # Loads response as JSON
        directions = json.loads(response)
        # print(directions)
        temp = []
        time = []
        for k in range(0, len(starts)):
            temp.append(directions['rows'][0]['elements'][k]['distance']['value'] / 10)  # shrink size by 10
            time.append(directions['rows'][0]['elements'][k]['duration']['value'] / 60)  # convert sec to min
        dis_mx.append(temp)
        time_cost.append(time)
    # Construct for location matrix
    location = []
    x = []
    y = []
    ends_geo = 'place_id=' + locations[0]
    for j in range(1, len(locations)):
        ends_geo += '|place_id=' + locations[j]
    # geocoding  https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
    # https://maps.googleapis.com/maps/api/geocode/json?place_id=ChIJOwE7_GTtwokRFq0uOwLSE9g&key=AIzaSyB_Ft9gDmURfbNOy5khTul1IstGeWG1qe4
    endpoint_geo = 'https://maps.googleapis.com/maps/api/geocode/json?'
    api_key_geo = os.getenv('API_KEY_GEO')
    for l in locations:
        nav_request_geo = 'place_id={}&key={}'.format(l, api_key_geo)
        request_geo = endpoint_geo + nav_request_geo
        print(request_geo)
        response = urllib.request.urlopen(request_geo).read()
        loc = json.loads(response)
        # print(response)
        x.append(loc['results'][0]['geometry']['location']['lng'])
        y.append(loc['results'][0]['geometry']['location']['lat'])
    location.append(x)
    location.append(y)
    data = {'distance_matrix': dis_mx, 'capacities': capacities, 'origins': origins, 'location': location,
            'time_cost': time_cost, 'locations_txt': locations_text, 'email_list': email_list, 'phone_num': phone_num,
            'name': user_name}
    # print(data)
    return data
