import json
import urllib.request
from app import User
import os
from database import db_session

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
    locations = [os.getenv('DEST_ID')]
    locations_text = ["HA"]
    email_list = ["HA"]
    phone_num = ["123"]
    user_name = ["dest"]
    # if you declare your table as a class:
    #   all_users = User.query.all()  # for locations matrix
    all_users = db_session.query(User).all()  # for locations matrix
    i = 1
    for user in all_users:
        if not user.will_present:
            continue
        user.will_present = False
        if getattr(user, 'is_driver'):
            capacities.append(getattr(user, 'capacity'))
            origins.append(i)
        locations.append(getattr(user, 'address_id'))
        locations_text.append(getattr(user, 'address_show_txt'))
        email_list.append(getattr(user, 'email'))
        db_phone = getattr(user, 'phone_number')
        phone_num.append('(' + db_phone[:3] + ')' + db_phone[3:6] + '-' + db_phone[6:])
        user_name.append(getattr(user, 'name'))
        i += 1
    db_session.commit()
    # Convert locations
    # Google Maps Directions API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    api_key_distance_matrix = os.getenv('API_KEY_DIS')  # my api key do not share!!
    # Generate origins and destinations

    # origin = locations[0].replace(',', '')
    # origin = origin.replace(' ', '+')
    # origin = 'Toronto'
    starts = []
    for k in range(0, len(locations)):
        starts.append('place_id:' + locations[k])
    ends = 'place_id:' + locations[0]
    for j in range(1, len(locations)):
        ends += '|place_id:' + locations[j]
    destination = 'ChIJ6zWFnZIUkFQRoyu4AXksdGs|place_id=ChIJscQF-bNqkFQRqrFa919Xv5Y'
    dis_mx = []
    time_cost = []
    for w in starts:
        # Building the URL for the request
        nav_request = 'origins={}&destinations={}&key={}'.format(w, ends, api_key_distance_matrix)
        request = endpoint + nav_request
        print(request)
        # Sends the request and reads the response.
        response = urllib.request.urlopen(request).read()
        # Loads response as JSON
        directions = json.loads(response)
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
    # URL example:
    # geocoding  https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY

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
    # https: // maps.googleapis.com / maps / api / staticmap?center = Brooklyn + Bridge, New + York, NY&zoom=13&size
    # =600x300 & maptype = roadmap & markers = color:blue % 7Clabel: S % 7C40.702147, 74.015794 & markers =
    # color:green % 7Clabel: G % 7C40.711614, -74.012318 & markers = color:red % 7Clabel: C % 7C40.718217,
    # -73.998284 & key = YOUR_API_KEY
    data = {'distance_matrix': dis_mx, 'capacities': capacities, 'origins': origins, 'location': location,
            'time_cost': time_cost, 'locations_txt': locations_text, 'email_list': email_list, 'phone_num': phone_num,
            'name': user_name}
    return data


def get_and_print():
    all_users = db_session.query(User).all()
    print(
        'id' + '\t' + 'name' + '\t' + 'email' + '\t' + '\t' + 'is_driver' + '\t' + 'will_present' + '\t' + 'capacity' + '\t' +
        'phone_number' + '\t' + 'address_show_txt' + '\n')
    for user in all_users:
        print(
            str(user.id) + '\t' +
            str(user.name) + '\t' +
            str(user.email) + '\t' + '\t' +
            str(user.is_driver) + '\t' +
            str(user.will_present) + '\t' +
            str(user.capacity) + '\t' +
            str(user.phone_number) + '\t' +
            str(user.address_show_txt) + '\n')
