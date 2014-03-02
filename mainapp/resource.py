from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.resources import Resource
import urlparse
import json
from django.contrib.auth.models import User
from datetime import datetime

'''
Uses Tastypie for providing Restful API
Can be tried with url for API documentation at: /api/doc
'''


class urlencodeSerializer(Serializer):
    '''
    URL Encode Serializer class for the resource classes
    '''    
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
    }

    def from_urlencode(self, data, options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v) > 1 else v[0])
                  for k, v in urlparse.parse_qs(data).iteritems())
        
        return qs

    def to_urlencode(self, content):
        pass


class ReturnNext(Resource):
    '''
    Resource class for photos
    '''    
    class Meta:
        resource_name = 'photo'
        object_class = DynamoObject
        always_return_data = True
        filtering = {
            'ratings': ['exact',],
            'type': ['exact', ],
            'parent_id': ['exact',],
            "photo_id": ['exact', ],
            "ratings": ['exact', ],
        }

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        try:
            kwargs['pk'] = bundle_or_obj.data['id']
        except:
            pass
        return kwargs

    def get_object_list(self, request):

        table = self.get_table()
        items = table.scan()
        results = []
        for item in items:
            results.append(DynamoObject(initial=item))

        return results

    def obj_get_list(self, bundle, **kwargs):
        '''
        Returns all photos from dynamoDB
        '''
        table = self.get_table()

        items = table.query(type__eq = "Homedesign", photo_id__gte = 1, limit= 20, consistent = True )
        my_items = []
        for item in items:
            my_items.append(DynamoObject(initial=dict(item)))

        return my_items

    def dehydrate(self, bundle):
        for item in bundle.obj.to_dict().iteritems():
            bundle.data[item[0]] = item[1]
        return bundle

    def obj_get(self, request=None, **kwargs):
        '''
        Returns (GET) a specific photo by given id
        '''
        item_id = kwargs['pk']
        table = self.get_table()
        item = table.get_item(type='Homedesign', photo_id = int(item_id), consistent = True)
        # find greatest item
        greatest_item = table.query(type__eq='Homedesign', limit = 1, consistent = True)
        greatest_item = [i for i in greatest_item]
        greatest_item_id = greatest_item[0]['photo_id']
        item = dict(item)
        if int(item_id) == int(greatest_item_id):
            item['next_url'] = ''
        else:
            next_item = table.get_item(type='Homedesign', photo_id = int(item_id) + 1, consistent = True)
            item['next_url'] = get_next_url(next_item['photo'])
        return DynamoObject(initial=dict(item))

    def obj_create(self, bundle, request=None, **kwargs):
        form = VideoForm(bundle.data)
        returned_id = form.save()
        table = self.get_table()
        item = table.get_item(
            hash_key=returned_id,
        )
        bundle.data = item
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        return self.obj_create(bundle, request, **kwargs)


class Rating(Resource):
    '''
    Resource class for rating of photos
    '''    
    def get_table(obj):
        table = Table(TABLE_NAME_2)
        return table

    class Meta:
        resource_name = 'rating'
        serializer = urlencodeSerializer()
        object_class = DynamoObject
        always_return_data = True
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        try:
            kwargs['pk'] = bundle_or_obj.data['id']
        except:
            pass
        return kwargs

    def get_object_list(self, request):

        table = self.get_table()
        items = table.scan()
        results = []
        for item in items:
            results.append(DynamoObject(initial=item))

        return results

    def obj_get_list(self, bundle, **kwargs):
        '''
        Returns greatest photo_id rated by user
        '''
        table = self.get_table()
        ### need to get user_id from view
        user_id = bundle.request.user.id
        items = table.query(user_id__eq = user_id, limit= 1 , consistent = True)
        items = [i for i in items]
        my_items = []
        if len(items) == 0:
            my_items.append(DynamoObject(initial={"photo_id": "0"}))
        else:
            for item in items:
                my_items.append(DynamoObject(initial=dict(item)))
        return my_items

    def dehydrate(self, bundle):
        for item in bundle.obj.to_dict().iteritems():
            bundle.data[item[0]] = item[1]
        return bundle

    def obj_get(self, request=None, **kwargs):
        item_id = kwargs['pk']
        table = self.get_table()
        ratings_list = table.scan(photo_id__eq=int(item_id))
        ratings_list = [i for i in ratings_list]
        
        item = {}
        user_ids = ""
        for eachrating in ratings_list:
            if user_ids =="":
                user_ids = str(eachrating['user_id'])
            else:
                user_ids = user_ids + " " + str(eachrating['user_id'])
        item['user_ids'] = user_ids
        return DynamoObject(initial=dict(item))

    def obj_create(self, bundle, request=None, **kwargs):
        '''
        Creates ratings (POST) for photo
        '''
        putdata = bundle.data
        putdata['ratings'] = int(putdata['ratings'])
        putdata['photo_id'] = int(putdata['photo_id'])
        putdata['parent_id'] = int(putdata['parent_id'])
        putdata['user_id'] = int(putdata['user_id'])
        putdata['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # datetime.strptime(datetimestring, "%Y-%m-%d %H:%M:%S")
        
        send_msg(str(putdata))
        # print putdata
        # table = self.get_table()
        # table.put_item(data= putdata)
        item = table.get_item(user_id = putdata['user_id'], photo_id = putdata['photo_id'], consistent = True)
        bundle.data = item
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        return self.obj_create(bundle, request, **kwargs)
