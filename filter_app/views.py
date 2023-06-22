from django.shortcuts import render
from django.http import JsonResponse
from user.models import Society
from django.db.models import Count
from django.db.models.functions import ExtractYear


def reg_soc(request):
    states = Society.objects.values_list('state', flat=True).distinct()
    society_types = Society.objects.values_list('society_type', flat=True).distinct()
    registration_years = Society.objects.dates('date_joined', 'year', order='DESC')

    if request.method == 'GET':
        state = request.GET.get('state', '')
        district = request.GET.get('district', '')
        society_type = request.GET.get('society_type', '')
        registration_year = request.GET.get('registration_year', '')

        filtered_data = Society.objects.all()

        if state:
            filtered_data = filtered_data.filter(state=state)

        if district:
            filtered_data = filtered_data.filter(district=district)

        if society_type:
            filtered_data = filtered_data.filter(society_type=society_type)

        if registration_year:
            filtered_data = filtered_data.filter(date_joined__year=registration_year)
    else:
        filtered_data = Society.objects.all()  # Show all data when no filters are applied

    context = {
        'states': states,
        'society_types': society_types,
        'registration_years': registration_years,
        'filter_data': filtered_data
    }

    return render(request, 'filter/reg_soc.html', context)

def bank_data(request):
    cooperative_banks = Society.objects.filter(society_type="Cooperative Bank")
    
    context = {
        'banks': cooperative_banks
    }
    
    return render(request, 'filter/bank.html', context)

def get_districts_view(request):
    state = request.GET.get('state', '')
    districts = Society.objects.filter(state=state).values_list('district', flat=True).distinct()
    return JsonResponse({'districts': list(districts)})

def state_wise(request):
    total_societies = Society.objects.count()
    all_states = Society.objects.values_list('state', flat=True).distinct()
    state_filter = request.GET.get('state', '')

    if state_filter:
        state_data = Society.objects.filter(state=state_filter).values('state').annotate(count=Count('id'))
    else:
        state_data = Society.objects.values('state').annotate(count=Count('id'))
    
    total_societies_state = sum(item['count'] for item in state_data) 

    context = {
        'all_states': all_states,
        'state_data': state_data,
        'total_societies': total_societies,
        'total_state':total_societies_state
    }

    return render(request, 'filter/state_wise.html', context)

def cal_wise(request):
    all_years = Society.objects.dates('date_joined', 'year', order='DESC')
    selected_year = request.GET.get('year')
    total_societies = Society.objects.count()

    if selected_year:
        year_data = Society.objects.filter(date_joined__year=int(selected_year)).annotate(calendar_year=ExtractYear('date_joined')).values('calendar_year').annotate(count=Count('id')).order_by('calendar_year')
    else:
        year_data = Society.objects.annotate(calendar_year=ExtractYear('date_joined')).values('calendar_year').annotate(count=Count('id')).order_by('calendar_year')
    
    total_societies_state = sum(item['count'] for item in year_data)
    context = {
        'all_years': all_years,
        'year_data': year_data,
        'selected_year': selected_year,
        'total_societies': total_societies,
        'total_state':total_societies_state
    }

    return render(request, 'filter/cal_wise.html', context)