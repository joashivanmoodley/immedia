from django.core.management.base import NoArgsCommand
import foursquare
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth import OAuthHandler

from image.models import Location, LandMark, Image


class Command(NoArgsCommand):

    def get_land_mark(self):
        '''
        Get a list of images based pre-defined locations.
        Land marks and Images are accessed via the foursquare and 500px apis respectively.
        https://github.com/500px/api-documentation/
        https://developer.foursquare.com/docs/
        run python manage.py get_land_mark
        to import this data.
        '''
        default_locations = ['New York', 'Durban', 'Sydney']
        client_id = 'FJ3DPZHYKN2DWSGBFQFCTYZSO0QQFQWENMPG041GC1HMHN5R'
        client_secret = 'CQ2LADABJOEI4R5UTKUNXSCF0VT4GBQEZBJVY4OCLLV5CY1W'
        redirect_uri = 'http://fondu.com/oauth/authorize'
        CONSUMER_KEY = 'RWABV8oGpEnZff17T3J7FM417m5l0NrO5zeQfrrF'
        CONSUMER_SECRET = 'C2ppB7O2NKXhzAZgK7N6Gd0rQL6aJI5OvQimysXG'

        handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        api = FiveHundredPXAPI(handler)
        client = foursquare.Foursquare(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri)
        for location in default_locations:
            print "Getting Location Data For %s" % location
            data = client.venues.search(params={'near': location, 'limit': 1})
            name = data['venues'][0]['name']
            contact = data['venues'][0]['contact']
            data = data['venues'][0]['location']

            country = data['country'] if 'iNingizimu Afrika' != data['country'] else 'South Africa'
            province = data['state'] if 'state' in data else 'Unknown'
            region = data['city'] if 'city' in data else location
            country_code = data['cc'] if 'cc' in data else 'Unknown'
            latitude = data['lat'] if 'lat' in data else 'Unknown'
            longitude = data['lng'] if 'lng' in data else 'Unknown'

            location_obj, created = Location.objects.get_or_create(
                country=country,
                province=province,
                region=region,
                cc=country_code,
                latitude=latitude,
                longitude=longitude
            )

            address = data['formattedAddress']
            latitude = data['lat']
            longitude = data['lng']

            if 'formattedPhone' in contact:
                number = contact['formattedPhone']
            else:
                number = None

            print "Getting Land Mark Data For %s" % location
            land_mark, created = LandMark.objects.get_or_create(
                name=name,
                address=address[0],
                latitude=latitude,
                longitude=longitude,
                phone_number=number,
                location=location_obj
            )

            print "Getting Image Data For %s" % location
            json = api.photos_search(
                only="City and Architecture,Landscapes,Nature,Travel,Urban Exploration,Street, Commercial",
                rpp=10,
                term=land_mark.name, geo='%s,%s,5km' % (land_mark.latitude, land_mark.longitude),
                consumer_key=CONSUMER_KEY
            )

            if json['photos']:
                for data in json['photos']:
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

    def handle_noargs(self, **options):
        self.get_land_mark()
