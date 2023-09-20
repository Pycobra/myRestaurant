from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import login, logout

from apps.product.models import Product, Category
from apps.checkout.models import PaymentSelections
from apps.account.forms import UserLoginForm, RegistrationForm, UserAddressForm

from apps.checkout.models import DeliveryOptions
from apps.order.models import Address  
from apps.vendor.models import Vendor    



def frontpage(request):
    session = request.session
    mydeliveryopt = {}
    mydeliveryadd = {}
    deliveryoptions = {}
    addressoptions = {}
    myPaymentOpt = {}
    # del session
    # print(session["address"])
    if "purchase" in request.session:
        delivery_id = session["purchase"]['delivery_id']
        mydeliveryopt = DeliveryOptions.objects.get(id=delivery_id)
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True).exclude(id=delivery_id)
    if "address" in request.session:
        address_id = session["address"]['address_id']
        mydeliveryadd = Address.objects.get(id=address_id)
        addressoptions = Address.objects.all().exclude(id=address_id)
    if "payment" in request.session:
        payment_id = session["payment"]['payment_id']
        myPaymentOpt = PaymentSelections.objects.get(id=payment_id)
    paymentOptions = PaymentSelections.objects.all()
    #all_products = Product.objects.prefetch_related("product_images").filter(is_active=True, in_stock=True).order_by('-created_at')
    all_products = Product.objects.filter(is_active=True, in_stock=True).order_by('-created_at')
    # categories = Category.objects.filter(level=0)
    cat_list = []
    for i in all_products:
        cat_list.append(i.category)
    categories = list(set(cat_list))

    vendor_categories = Category.objects.filter(level=0)
    all_vendor = Vendor.objects.all()
    return render(request, 'core/frontpage.html', {'all_products': all_products, 'categories':categories, 
                                                    'loginForm':UserLoginForm, 'registerform':RegistrationForm,
                                                   'addressForm':UserAddressForm, 'mydeliveryopt':mydeliveryopt, 'mydeliveryadd':mydeliveryadd,
                                                   'deliveryoptions':deliveryoptions,"addressoptions":addressoptions,
                                                   'images': ['food-cover1','food-cover2','food-cover3','food-cover4'], 
                                                   'vendor_categories':vendor_categories, 'all_vendor':all_vendor, 
                                                   'myPaymentOpt': myPaymentOpt, 'paymentOptions': paymentOptions,
                                                    # 'vendor_product': product
                                                    })




# # GOOGLE GEO LOCATION CODE = GEOCODING
# from urllib.parse import urlencode
# import requests
# GOOGLE_API_KEY = "put your api key"

# class GoogleMapsClient(object):
#     lat = None
#     lng = None
#     data_type = 'json'
#     location_query = None
#     api_key=None

#     def __init__(self, api_key=None, address_or_postal_code=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if api_key == None:
#             raise Exception("API key is required")
#         self.api_key = api_key
#         self.location_query = address_or_postal_code
#         if self.location_query != None:
#             self.extract_lat_lng()

#     # GEOCODING API
#     def extract_lat_lng(self, location=None):
#         loc_query = self.location_query
#         if location != None:
#             loc_query = location
#         endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
#         params = {"address": loc_query, "key":self.api_key}
#         r = self.place_request(endpoint=endpoint, params=params)
#         # params_encoded = urlencode(params)
#         # url = f'{endpoint}?{params_encoded}'
#         # r = request.get(url)
#         # if r.status_code not in range(200, 299):
#         #     return {}
#         latlng = {}
#         try:
#             latlng = r.json()['results'][0]['geometry']['location']
#         except:
#             pass
#         lat,lng = latlng.get("lat"), latlng.get("lng")
#         self.lng = lng
#         self.lat = lat
#         return lng, lat

#     def search_nearby_place(self, radius= 1500, location=None):
#         lat, lng = self.lat, sel.lng
#         if location != None:
#             lat, lng = self.extract_lat_lng(location=location)
#         endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
#         params = {
#             'key': self.api_key,
#             'location': f"{lat},{lng}",
#             'keyword': "mexican food",
#             'radius': radius
#         }
#         r =  self.place_request(endpoint=endpoint, params=params)
#         return r
#         # params_encoded = urlencode(params)
#         # url = f"{endpoint}?{params_encoded}"
#         # r = requests.get(purl)
#         # if r.status_code not in range(200, 299):
#         #     return {}
#         # return r.json()
#     def detail(self, place_id= "ChIJN1X0KcDC3j4ARzal-5j-p-FY"):
#         endpoint = f"https://maps.googleapis.com/maps/api/place/detail/{self.data_type}"
#         params = {
#             'place': f"{place_id}",    
#             'key': self.api_key,
#             'fields': "formatted_phone_number,name,rating,formatted_address"

#         }
#         r = self.place_request(endpoint=endpoint, params=params)
#         return r
#         # params_encoded = urlencode(params)
#         # url = f"{endpoint}?{params_encoded}"
#         # r = requests.get(url)
#         # if r.status_code not in range(200, 299):
#         #     return {}
#         # return r.json()

#     def place_request(self, endpoint=None, params=None):
#         params_encoded = urlencode(params)
#         url = f"{endpoint}?{params_encoded}"
#         r = requests.get(url)
#         if r.status_code not in range(200, 299):
#             return {}
#         return r.json()
# client = GoogleMapsClient(api_key=GOOGLE_API_KEY, address_or_postal_code="Newport Beach, CA")
# print(client.lat, client.lng)
# # client.search_nearby_place('Tacos', location="Newport Beach")
# # client.detail(place_id="Newport Beach")

# # # here we work with url dictionary, first we single out the query, 
# # # next we break the query into tuple wrapped in a list, 
# # # lastly we put them back into dict
# # from urllib.parse import urlparse, parse_qsl
# # to_parse = url #'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheater+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY'
# # parsed_url = urlparse(to_parse)
# # query_string = parsed_url.query
# # query_tuple = parse_qsl(query_string)
# # query_dict = dict(query_tuple)
# # endpoint = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

# # # ============== PLACE API =========================
# # # Part A = Gives only one location which is closest to my speciied lng & lat
# # lat, lng = 37.42230960000001, -122.0846244
# # base_endpoint_places = "https://maps.googleapis.com/maps/api/place/findplacefomtext/json"
# # params = {
# #     'key': api_key,
# #     'input': "mexican food",
# #     'inputtype': "textquery",
# #     'fields': "place_id,formatted_address,name,geometry,permanently_closed"
# # }
# # locationbias = f"point:{lat},{lng}"
# # use_circular - False
# # if use_circular:
# #     radius = 1000
# #     locationbias = f"circle:{radius}@{lat},{lng}"
# # params['locationbias'] = locationbias

# # params_encoded = urlencode(params)
# # places_endpoint = f"{base_endpoint_places}?{params_encoded}"
# # r = requests.get(places_endpoint)
# # r.json()


# # # Part B = finds multiple places nearby specified location
# # base_endpoint_places2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# # params2 = {
# #     'key': api_key,
# #     'location': f"{lat},{lng}"
# #     'keyword': "mexican food",
# #     'radius': 1500
# # }
# # params_encoded2 = urlencode(params2)
# # places_endpoint2 = f"{base_endpoint_places2}?{params_encoded2}"
# # r2 = requests.get(places_endpoint2)
# # r2.json()

# # # Part B(i) = finds detail of specified place
# # place_id = "ChIJN1X0KcDC3j4ARzal-5j-p-FY"
# # detail_base_endpoint = "https://maps.googleapis.com/maps/api/place/detail/json"
# # detail_params = {
# #     'place': f"{place_id}",    
# #     'key': api_key,
# #     'fields': "formatted_phone_number,name,rating,formatted_address"

# # }
# # detail_params_encoded = urlencode(detail_params)
# # detail_url = f"{detail_base_endpoint}?{detail_params_encoded}"
# # r = requests.get(detail_url)
# # r.json()






