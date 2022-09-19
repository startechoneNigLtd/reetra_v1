from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .productAnalysis import product_analysis as PA
from .serviceAnalysis import service_analysis as SA

from productReceipt.models import Receipt_No as PRN
from serviceReceipt.models import Receipt_No as SRN

# Create your views here.
import requests, json
import math

#Dashboard display
@login_required
def dashboard(request):


            
    response = requests.get('http://ipinfo.io/json')
    xy =response.json()
    print(xy['city'])
    # Enter your API key here
    api_key = "dfed3d3a320c802c55f516734861efb5"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = xy['city']

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
    print(x)
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"] - 273

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        #print(current_humidity)
        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["icon"]

       

    else:
        print(" City Not Found ")

  
    srn = SRN.objects.filter(user = request.user)
    prn = PRN.objects.filter(user = request.user)
    context = {
        'weather_description': "http://openweathermap.org/img/w/" + weather_description + ".png",
        'temperature': round(current_temperature,4),
        'total': srn.count() + prn.count(),
        'total_receipt': PA()['total_receipt'] + SA()['total_receipt'],
        'today_receipt': PA()['today_receipt'] + SA()['today_receipt'],
        'this_week': PA()['this_week'] + SA()['this_week'],
        'this_month': PA()['this_month'] + SA()['this_month'],

        'week_analysis_count': [PA()['week_analysis_count'][0]+SA()['week_analysis_count'][0],
                                PA()['week_analysis_count'][1]+SA()['week_analysis_count'][1],
                                PA()['week_analysis_count'][2]+SA()['week_analysis_count'][2],
                                PA()['week_analysis_count'][3]+SA()['week_analysis_count'][3],
                                PA()['week_analysis_count'][4]+SA()['week_analysis_count'][4],
                                PA()['week_analysis_count'][5]+SA()['week_analysis_count'][5],
                                PA()['week_analysis_count'][6]+SA()['week_analysis_count'][6]
                                ],
        
        'month_analysis_count':[PA()['month_analysis_count'][0]+SA()['month_analysis_count'][0],
                                PA()['month_analysis_count'][1]+SA()['month_analysis_count'][1],
                                PA()['month_analysis_count'][2]+SA()['month_analysis_count'][2],
                                PA()['month_analysis_count'][3]+SA()['month_analysis_count'][3],
                                PA()['month_analysis_count'][4]+SA()['month_analysis_count'][4],
                                PA()['month_analysis_count'][5]+SA()['month_analysis_count'][5],
                                PA()['month_analysis_count'][6]+SA()['month_analysis_count'][6],
                                PA()['month_analysis_count'][7]+SA()['month_analysis_count'][7],
                                PA()['month_analysis_count'][8]+SA()['month_analysis_count'][8],
                                PA()['month_analysis_count'][9]+SA()['month_analysis_count'][9],
                                PA()['month_analysis_count'][10]+SA()['month_analysis_count'][3],
                                PA()['month_analysis_count'][11]+SA()['month_analysis_count'][11],
                                
                                ],

        'month_analysis_sales': [PA()['month_analysis_sales'][0]+SA()['month_analysis_sales'][0],
                                PA()['month_analysis_sales'][1]+SA()['month_analysis_sales'][1],
                                PA()['month_analysis_sales'][2]+SA()['month_analysis_sales'][2],
                                PA()['month_analysis_sales'][3]+SA()['month_analysis_sales'][3],
                                PA()['month_analysis_sales'][4]+SA()['month_analysis_sales'][4],
                                PA()['month_analysis_sales'][5]+SA()['month_analysis_sales'][5],
                                PA()['month_analysis_sales'][6]+SA()['month_analysis_sales'][6],
                                PA()['month_analysis_sales'][7]+SA()['month_analysis_sales'][7],
                                PA()['month_analysis_sales'][8]+SA()['month_analysis_sales'][8],
                                PA()['month_analysis_sales'][9]+SA()['month_analysis_sales'][9],
                                PA()['month_analysis_sales'][10]+SA()['month_analysis_sales'][3],
                                PA()['month_analysis_sales'][11]+SA()['month_analysis_sales'][11],
                                
                                ],
        
    }
    
    return render(request, 'dashboard/dashboard.html', context)