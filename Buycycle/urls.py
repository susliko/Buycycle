from django.urls import path

from Buycycle.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
]