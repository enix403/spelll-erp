from django.urls import path, include
from django.http import JsonResponse

from app.core.manage import apiviews as manage_views
from app.core.authentication import apiviews as auth_views
from app.core.sections import apiviews as section_views

def not_implemented(req):
    return JsonResponse({'error': 'This action is not implemented yet'})


urlpatterns = [
    path("", not_implemented),

    path('api/', include([
        path('stations/', manage_views.station_list),
        path('station/create/', manage_views.station_create),
        path('station/<int:station_id>/update/', manage_views.station_update),

        path('colleges/', manage_views.college_list),
        path('college/create/', manage_views.college_create),
        path('college/<int:college_id>/update/', manage_views.college_update),

        path('college/<int:college_id>/sections/', section_views.section_list),
        path('section/create/', section_views.section_create),
        path('section/<int:section_id>/update/', section_views.section_update),

        path('auth/login/', auth_views.login),
        path('auth/refresh/', auth_views.get_access_token),
        path('auth/user-info/', auth_views.get_user_info),
    ]))
]