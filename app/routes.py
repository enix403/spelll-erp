from django.urls import path, include
from django.http import JsonResponse

from app.core.manage import apiviews as manage_views
from app.core.authentication import apiviews as auth_views

def not_implemented(req):
    return JsonResponse({'error': 'This action is not implemented yet'})


urlpatterns = [
    path("", not_implemented),

    path('api/', include([
        path('stations/', manage_views.station_list),
        path('stations/create/', manage_views.station_create),
        path('stations/<int:station_id>/update/', manage_views.station_update),

        path('auth/login/', auth_views.login),
        path('auth/refresh/', auth_views.get_access_token),
    ]))
]

"""
from django.urls import path, include
from django.http import JsonResponse

from .home import index

from app.core.manage import views as manage_views

def not_implemented(req):
	return JsonResponse({'error': 'This action is not implemented yet'})

urlpatterns = [
    path("", index),

    path('manage/', manage_views.index, name="manage"),
    path('api/add/station/', manage_views.Action_CreateStation.as_view(), name="add-station"),
    path('api/add/college/', manage_views.Action_CreateCollege.as_view(), name="add-college"),

]
"""