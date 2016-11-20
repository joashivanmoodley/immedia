from django.shortcuts import render
import foursquare
from image.models import Location, Image, LandMark
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth import OAuthHandler

CONSUMER_KEY = 'RWABV8oGpEnZff17T3J7FM417m5l0NrO5zeQfrrF'
CONSUMER_SECRET = 'C2ppB7O2NKXhzAZgK7N6Gd0rQL6aJI5OvQimysXG'
headers = {}


def view_locations(request):
    '''
    View to return all locations that are captured in the db.
    It will also  try to pull a location from foursquare if its not founded in local db.
    '''
    template_vars = {}
    locations = Location.objects.all()
    location_check = True
    if request.POST.get('search'):
        location = request.POST.get('search', None)

        if search_location(location)['venues']:
            location_data = search_location(location)['venues'][0]['location']
            country = location_data['country'] if 'iNingizimu Afrika' != location_data['country'] else 'South Africa'
            province = location_data['state'] if 'state' in location_data else 'Unknown'
            region = location_data['city'] if 'city' in location_data else location
            country_code = location_data['cc'] if 'cc' in location_data else 'Unknown'
            latitude = location_data['lat'] if 'lat' in location_data else 'Unknown'
            longitude = location_data['lng'] if 'lng' in location_data else 'Unknown'

            location_obj, created = Location.objects.get_or_create(
                country=country,
                province=province,
                region=region,
                cc=country_code,
                latitude=latitude,
                longitude=longitude
            )
            if not created:
                locations = locations.filter(
                    country=country,
                    province=province,
                    region=region,
                    )
            else:
                search_location(location, True, location_obj.id)
        else:
            location_check = False

    template_vars['locations'] = locations
    template_vars['location_check'] = location_check
    return render(request, 'view_locations.html', template_vars)


def list_images(request, location_id):
    '''
    View used to list all images for a give location.
    '''
    template_vars = {}
    location_name = Location.objects.get(id=location_id)
    images = Image.objects.filter(land_mark__location__id=location_id)
    template_vars['images'] = images
    template_vars['location_name'] = location_name
    return render(request, 'list_images.html', template_vars)


def view_image(request, image_id):
    '''
    View to return details about specific image.
    '''
    template_vars = {}
    image = Image.objects.get(id=image_id)
    template_vars['image'] = image
    return render(request, 'view_image.html', template_vars)


def search_location(location, save_landmark=False, id=None):
    '''
    Function tries to match a given location to whats in the db, if not found it will search
    Foursquare API for the location and then save to db.
    '''
    client_id = 'FJ3DPZHYKN2DWSGBFQFCTYZSO0QQFQWENMPG041GC1HMHN5R'
    client_secret = 'CQ2LADABJOEI4R5UTKUNXSCF0VT4GBQEZBJVY4OCLLV5CY1W'
    redirect_uri = 'http://fondu.com/oauth/authorize'
    client = foursquare.Foursquare(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    land_marks = client.venues.search(params={'near': location, 'limit': 1})
    if not land_marks:
        land_marks = client.venues.search(params={'ll': location, 'limit': 1})
    if save_landmark:
        for l in land_marks['venues']:
            name = l['name']
            address = l['location']['formattedAddress']
            latitude = l['location']['lat']
            longitude = l['location']['lng']

            if 'formattedPhone' in l['contact']:
                number = l['contact']['formattedPhone']
            else:
                number = None

            landmark_obj, created = LandMark.objects.get_or_create(
                name=name,
                phone_number=number,
                address=address[0],
                latitude=latitude,
                longitude=longitude,
                location=Location.objects.get(id=id)
            )
            get_location_images(landmark_obj.id)

    return land_marks


def get_location_images(land_mark_id):
    '''
    Function used to hooked in 500px API to get images based on location land mark.
    '''
    CONSUMER_KEY = 'RWABV8oGpEnZff17T3J7FM417m5l0NrO5zeQfrrF'
    CONSUMER_SECRET = 'C2ppB7O2NKXhzAZgK7N6Gd0rQL6aJI5OvQimysXG'

    handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = FiveHundredPXAPI(handler)
    land_mark = LandMark.objects.get(id=land_mark_id)

    photo = api.photos_search(
        rpp=10,
        only="City and Architecture,Landscapes,Nature,Travel,Urban Exploration,Street, Commercial",
        term=land_mark.name, geo='%s,%s,5km' % (land_mark.latitude, land_mark.longitude),
        consumer_key=CONSUMER_KEY
    )

    if not photo['photos']:
        photo = api.photos_search(
            rpp=10,
            geo='%s,%s,5km' % (land_mark.latitude, land_mark.longitude),
            consumer_key=CONSUMER_KEY
        )

    if photo['photos']:
        for data in photo['photos']:
            images = data['images'][0]
            image_url = images['url']
            image_format = images['format']
            description = data['description']
            date_created = data['created_at']
            owner = data['user']['fullname']
            Image.objects.get_or_create(
                date_added=date_created, land_mark=land_mark,
                image=image_url, image_type=image_format,
                description=description, owner=owner
            )
