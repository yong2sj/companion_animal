from django.shortcuts import render
from django.http import HttpResponse
from urllib3 import HTTPResponse
import folium

def main(request):
    # 맵 객체 생성
    m = folium.Map(location=[5.6555, -0.1830], zoom_start=7)

    # html로 변환
    m = m._repr_html_()
    
    context = {
        'm':m
    }
    return render(request, "petmap/board_main.html", context)
