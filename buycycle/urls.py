from django.urls import path

from buycycle.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
]