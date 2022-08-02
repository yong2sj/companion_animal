from django.shortcuts import render
from django.http import HttpResponse
from urllib3 import HTTPResponse
import folium

def main(request):
    m = folium.Map()
    m.save('map.html')
    context = {
        'm':m
    }
    return render(request, "petmap/board_main.html", context)
