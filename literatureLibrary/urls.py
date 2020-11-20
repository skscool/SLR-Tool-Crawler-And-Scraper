from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('ieee', views.ieee),
    path('springer', views.springer),
    path('scienceDirect', views.sciencedirect),
    path('acm', views.acm),
    path('fetchAll',views.fetchAll),
    path('fetchScienceDirect',views.fetchScienceDirect),
    path('fetchIEEE',views.fetchIEEE),
    path('fetchACM',views.fetchACM),
    path('fetchFilters',views.fetchFilters),
    path('fetchBibTexFromSpringer',views.fetchBibTexFromSpringer),
    path('isSearchValid',views.isSearchValid)
]