from django.shortcuts import render

from app.models import (
    Admission,
    Discipline
)

from app.core.admissions import Level, InterAdmissionType

def is_pfy_amount_enabled(adm: Admission):
        return adm.level == Level.INTER and \
               adm.adm_type == InterAdmissionType.Regular and \
               adm.semOrYear == 1


def make_disp_rows(level):
    disciplines = Discipline.objects.filter(level=level)
    rows = []
    grand_total_count = 0
    grand_total_payable = 0
    grand_total_paid = 0
    grand_total_balance = 0
    for disp in disciplines:
        total_count = 0
        total_payable = 0
        total_paid = 0
        total_balance = 0
        for adm in Admission.objects.filter(discipline=disp): # type: Admission
            adm: Admission
            paid = adm.adm_amount
            if is_pfy_amount_enabled(adm):
                paid += adm.pfy_amount
            
            total_count += 1
            total_payable += adm.final_package
            total_paid += paid
            total_balance += adm.final_package - paid

        if total_count == 0:
            avg = 0
        else:
            avg = total_payable / total_count

        rows.append({
            'name': disp.name,
            'count': f'{total_count:,}',
            'payable': f'{total_payable:,}',
            'paid': f'{total_paid:,}',
            'balance': f'{total_balance:,}',
            'avg': f'{avg:,.2f}',
        })

        grand_total_count += total_count
        grand_total_payable += total_payable
        grand_total_paid += total_paid
        grand_total_balance += total_balance

    if grand_total_count == 0:
        avg = 0
    else:
        avg = grand_total_payable / grand_total_count

    stats = {
        'count': f'{grand_total_count:,}',
        'payable': f'{grand_total_payable:,}',
        'paid': f'{grand_total_paid:,}',
        'balance': f'{grand_total_balance:,}',
        'avg': f'{avg:,.2f}',
    }

    return rows, stats


def admission_summary_index(request):
    inter_rows, inter_stats = make_disp_rows(Level.INTER)
    bs_rows, bs_stats = make_disp_rows(Level.BS)
    
    return render(request, 'main/pages/adm-summary.html', {
        # 'rows': rows,
        # 'stats': stats
        'inter': {
            'rows': inter_rows,
            'stats': inter_stats
        },
        'bs': {
            'rows': bs_rows,
            'stats': bs_stats
        }
    })


# ============================ Ledger ============================



def get_ledger_context():
    students = []
    total_count = 0
    total_payable = 0
    total_paid = 0
    total_balance = 0

    for adm in Admission.objects.filter(level=Level.INTER).prefetch_related('discipline'): # type: Admission
        adm: Admission
        paid = adm.adm_amount
        if is_pfy_amount_enabled(adm):
            paid += adm.pfy_amount

        students.append({
            'name': adm.name,
            'father_name': adm.father_name,
            'phone': adm.phone,
            'disp': adm.discipline.name,
            'marks': adm.marks,
            # 'percent': str(adm.marks / 11) + "%",
            'percent': f'{adm.marks / 11:.2f}%',
            'fee': adm.full_fee,
            'disc': {
                'policy': adm.marks_based_disc,
                'discretion': adm.discretion_disc,
                'total': adm.marks_based_disc + adm.discretion_disc,
            },
            'final_package': adm.final_package,
            'paid': paid,
            'balance': adm.final_package - paid,
        })
        total_count += 1
        total_payable += adm.final_package
        total_paid += paid
        total_balance += adm.final_package - paid

    if total_count == 0:
        avg = 0
    else:
        avg = total_payable / total_count

    stats = {
        'count': f'{total_count:,}',
        'payable': f'{total_payable:,}',
        'paid': f'{total_paid:,}',
        'balance': f'{total_balance:,}',
        'avg': f'{avg:,.2f}',
    }

    return {
        'students': students,
        'total_stats': stats
    }


def student_ledger_index(request):
    return render(request, 'main/pages/student-ledger.html', get_ledger_context())