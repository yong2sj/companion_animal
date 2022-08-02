from .views import views
from django.urls import path


urlpatterns = [
    path("<int:board_id>", views.detail, name="detail"),
]
