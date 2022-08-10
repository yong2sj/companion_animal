import os
from django.shortcuts import render
from django.http import HttpResponse
from urllib3 import HTTPResponse
import pandas as pd
import folium

from config.settings import BASE_DIR

html = ""


def main(request):
    # 맵 객체 생성
    animal = pd.read_csv(os.path.join(BASE_DIR, "static", "data", "pythonproject.csv"))

    m = folium.Map(
        location=[37.536697, 126.998426], zoom_start=12.4, tiles="OpenStreetMap"
    )
    for index, row in animal.iterrows():
        html = (
            """
        <h1>"""
            + row["가게이름"]
            + """</h1>
        <p>주소 : """
            + row["상세주소"]
            + """</p>
        <p> 전화번호 : """
            + row["전화번호"]
            + """</p>
        <p>별점 : """
            + str(row["별점"])
            + """</p>"""
        )
        if row["구분"] == "카페":
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(html=html, max_width=2560),
                icon=folium.Icon(color="blue", icon="coffee", prefix="fa"),
            ).add_to(m)
        else:
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(html=html, max_width=2560),
                icon=folium.Icon(color="red", icon="glyphicon-plus-sign"),
            ).add_to(m)

    # html로 변환
    m = m._repr_html_()

    context = {"m": m}
    return render(request, "petmap/board_main.html", context)
