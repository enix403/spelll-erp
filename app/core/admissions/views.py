import json
import datetime
from dateutil.parser import parse as parse_date


from django.http.response import HttpResponse
from django.urls.base import reverse
from app.models.core import Discipline
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch

from app.utils.request_handling import get_bag, redirect_back

from app.models import (
    Discipline,
    FeeSlab,
    Admission,
    College
)

from app.models import College
from .constants import Level, InterAdmissionType, AdmissionSession, Gender

def make_structure(discipline):
    if discipline.fee_structures.count() == 0:
        return {'full_fee': 0, 'slabs': []}

    first = list(discipline.fee_structures.all())[0]
    # first = discipline.fee_structures.first()
    slabs = []

    for s in first.slabs.all():
        slabs.append({
            'name': s.name, 
            'index': s.index, 
            'marks': s.marks, 
            'amount': s.amount   
        })

    return {
        'full_fee': first.full_fee,
        'slabs': slabs
    }


def index(req, college_id):
    college = College.objects.filter(pk=college_id).first()

    disciplines = []
    # Artist.objects.prefetch_related()
    for d in Discipline.objects.prefetch_related('fee_structures', Prefetch('fee_structures__slabs', queryset=FeeSlab.objects.order_by('index'))):
        disciplines.append({
            'id': d.pk,
            'level': d.level,
            'name': d.name,
            'fee_structure': make_structure(d)
        })

    return render(req, "main/pages/admissions.html", {
        'server_data': {
            'college': {
                'id': college.pk,
                'name': college.name
            },
            'disciplines': disciplines,
            'constants': {
                'Level': {
                    'INTER': Level.INTER,
                    'BS': Level.BS,
                },
                'InterAdmissionType': {
                    'Regular': InterAdmissionType.Regular,
                    'PFY': InterAdmissionType.PFY,
                },
                'Gender': {
                    'Male': Gender.Male,
                    'Female': Gender.Female,
                },
                'AdmissionSession': {
                    'Morning': AdmissionSession.Morning,
                    'Evening': AdmissionSession.Evening,
                }
            },
            'urls': {
                'new_admission': reverse('new_admission')
            }
        },
    })

def new_admission(request):
    payload = json.loads(get_bag(request)['payload_json'])
    output = json.dumps(payload, indent=4)

    college_id = payload['college_id']
    gender = payload['gender']
    name = payload['name']
    cnic = payload['cnic']
    father_name = payload['father_name']
    father_cnic = payload['father_cnic']
    phone = payload['phone']
    date_of_birth = payload['date_of_birth']
    level = payload['level']
    discipline_id = payload['discipline_id']
    adm_session = payload['adm_session']
    adm_type = payload['adm_type']
    semOrYear = payload['semOrYear']
    marks = payload['marks']
    full_fee = payload['full_fee']
    marks_based_disc = payload['marks_based_disc']
    other_discount = payload['other_discount']
    discretion_disc = payload['discretion_disc']
    discretion_disc_reason = payload['discretion_disc_reason']
    # total_disc = payload['total_disc']
    pfy_amount = payload['pfy_amount']
    final_package = payload['final_package']
    num_installments = payload['num_installments']
    adm_amount = payload['adm_amount']

    discipline = Discipline.objects.filter(pk=discipline_id).first()
    college = College.objects.filter(pk=college_id).first()

    if not name or not cnic or not father_name or not father_cnic or not phone or not date_of_birth:
        return HttpResponse("Please fill all fields")

    admission = Admission()
    admission.college = college
    admission.name = name
    admission.gender = gender
    admission.cnic = cnic
    admission.father_name = father_name
    admission.father_cnic = father_cnic
    admission.phone = phone
    
    if isinstance(date_of_birth, str):
        dob = parse_date(date_of_birth)
    elif isinstance(date_of_birth, list):
        dob = parse_date(date_of_birth[0])

    else:
        return HttpResponse("Invalid date of birth")

    admission.date_of_birth = datetime.date(dob.year, dob.month, dob.day)
    # admission.date_of_birth = date_of_birth[0][0:10]
    admission.level = level
    admission.discipline = discipline
    admission.session = adm_session
    admission.adm_type = adm_type
    admission.semOrYear = semOrYear
    admission.marks = marks
    admission.full_fee = full_fee
    admission.marks_based_disc = marks_based_disc
    admission.discretion_disc = discretion_disc
    admission.discretion_disc_reason = discretion_disc_reason
    # admission.total_disc = marks_based_disc + discretion_disc
    admission.pfy_amount = pfy_amount
    admission.final_package = final_package
    admission.num_installments = num_installments
    admission.adm_amount = adm_amount
    try:
        admission.save()
    except Exception as e:
        print("\n\n=======================================================")
        print(e)
        print("=======================================================\n\n")
        return HttpResponse("An error occurred")
    # da = "2021-08-10T19:00:00.000Z"

    return redirect_back(request)

    """
    class Admission(BaseModel):
        name = models.CharField(max_length=255)
        gender = fields.PositiveTinyIntegerField()
        cnic = models.CharField(max_length=255)

        father_name = models.CharField(max_length=255)
        father_cnic = models.CharField(max_length=255)
        # school = models.CharField(max_length=255)
        # address = models.CharField(max_length=255)
        phone = models.CharField(max_length=255)
        date_of_birth = models.DateField()

        level = fields.PositiveTinyIntegerField()
        discipline = fields.make_foreign_key(Discipline, 'discipline_id')
        session = fields.PositiveTinyIntegerField()
        adm_type = fields.PositiveTinyIntegerField()
        semOrYear = fields.PositiveTinyIntegerField()

        marks = models.PositiveSmallIntegerField()

        full_fee = models.PositiveIntegerField()
        marks_based_disc = models.PositiveIntegerField()
        other_discount = fields.make_foreign_key(DiscountPreset, 'other_discount_id')
        discretion_disc = models.PositiveIntegerField()
        discretion_disc_reason = models.CharField(max_length=255)
        total_disc = models.PositiveIntegerField()

        pfy_amount = models.PositiveIntegerField()
        final_package = models.PositiveIntegerField()
        num_installments = fields.PositiveTinyIntegerField()
        adm_amount = models.PositiveIntegerField()
    """


    # return HttpResponse(output, content_type='text/plain')


