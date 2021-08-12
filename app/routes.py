from django.urls import path, include
from django.http import JsonResponse

from .home import index

from app.core.manage import views as manage_views
from app.core.admissions import views as adm_views
from app.core.reporting import views as reporting_views

def not_implemented(req):
	return JsonResponse({'error': 'This action is not implemented yet'})

urlpatterns = [
    path("", index),

    path('manage/', manage_views.index, name="manage"),
    path('api/add/station/', manage_views.Action_CreateStation.as_view(), name="add-station"),
    path('api/add/college/', manage_views.Action_CreateCollege.as_view(), name="add-college"),

    path('college/<int:college_id>/admission/', adm_views.index, name="admissions"),
    path('action/new_admission/', adm_views.new_admission, name="new_admission"),


    path('reports/adm-summary/', reporting_views.admission_summary_index, name="report-adm-summary"),
    path('reports/student-ledger/', reporting_views.student_ledger_index, name="report-student-ledger"),
]