from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count
import json
import csv
from django.http import HttpResponse

from .models import Survey, SurveyResponse, News


def is_admin(user):
    return user.is_staff or user.is_superuser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    surveys = Survey.objects.all().annotate(response_count=Count('responses'))
    news_items = News.objects.filter(is_active=True)[:5]
    total_responses = SurveyResponse.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    
    context = {
        'surveys': surveys,
        'news_items': news_items,
        'total_responses': total_responses,
        'total_users': total_users,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def user_dashboard(request):
    active_surveys = Survey.objects.filter(is_active=True)
    user_responses = SurveyResponse.objects.filter(user=request.user).values_list('survey_id', flat=True)
    news_items = News.objects.filter(is_active=True)[:5]
    
    context = {
        'surveys': active_surveys,
        'user_responses': list(user_responses),
        'news_items': news_items,
    }
    return render(request, 'user_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def create_survey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        questions_json = request.POST.get('questions')
        
        try:
            questions = json.loads(questions_json) if questions_json else []
            survey = Survey.objects.create(
                title=title,
                description=description,
                created_by=request.user,
                questions=questions
            )
            messages.success(request, 'Survey created successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error creating survey: {str(e)}')
    
    return render(request, 'create_survey.html')


@login_required
def view_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, is_active=True)
    has_responded = SurveyResponse.objects.filter(survey=survey, user=request.user).exists()
    
    context = {
        'survey': survey,
        'has_responded': has_responded,
    }
    return render(request, 'view_survey.html', context)


@login_required
@require_http_methods(["POST"])
def submit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, is_active=True)
    
    # Check if user already responded
    if SurveyResponse.objects.filter(survey=survey, user=request.user).exists():
        return JsonResponse({'success': False, 'message': 'You have already submitted this survey'})
    
    try:
        answers = json.loads(request.body)
        # Ensure all keys are strings for consistency
        formatted_answers = {}
        for key, value in answers.items():
            formatted_answers[str(key)] = value
        
        SurveyResponse.objects.create(
            survey=survey,
            user=request.user,
            answers=formatted_answers
        )
        return JsonResponse({'success': True, 'message': 'Survey submitted successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@user_passes_test(is_admin)
def survey_responses(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = SurveyResponse.objects.filter(survey=survey).select_related('user')
    
    # Process responses to include repeater sub-answers
    processed_responses = []
    for response in responses:
        if isinstance(response.answers, dict):
            new_answers = {}
            for key, value in response.answers.items():
                new_answers[str(key)] = value
            
            # Process repeater answers into a list format for easier template rendering
            repeater_data = {}
            for q in survey.questions:
                if q.get('type') == 'repeater':
                    q_id = str(q['id'])
                    source_id = str(q.get('repeat_source'))
                    # Member count always comes from the source question (e.g. "How many members?")
                    member_count = int(new_answers.get(source_id, 0) or 0)
                    if member_count > 0 and q.get('sub_questions'):
                        repeater_data[q_id] = []
                        for member_idx in range(member_count):
                            member_data = {
                                'member_number': member_idx + 1,
                                'answers': []
                            }
                            for sub_idx, sub_q in enumerate(q['sub_questions']):
                                sub_key = f"r{q['id']}_{member_idx}_{sub_idx}"
                                answer_value = new_answers.get(sub_key, '')
                                # Handle arrays (for checkboxes)
                                if isinstance(answer_value, list):
                                    answer_value = ', '.join(str(v) for v in answer_value)
                                member_data['answers'].append({
                                    'question': sub_q.get('text', f'Sub-Q{sub_idx+1}'),
                                    'answer': str(answer_value) if answer_value else '(No answer)'
                                })
                            repeater_data[q_id].append(member_data)
            
            response.processed_answers = new_answers
            response.repeater_data = repeater_data
        processed_responses.append(response)
    
    context = {
        'survey': survey,
        'responses': processed_responses,
    }
    return render(request, 'survey_responses.html', context)


@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff)
            messages.success(request, 'User created successfully!')
            return redirect('admin_dashboard')
    
    return render(request, 'add_user.html')


@login_required
@user_passes_test(is_admin)
def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        News.objects.create(title=title, content=content)
        messages.success(request, 'News added successfully!')
        return redirect('admin_dashboard')
    
    return render(request, 'add_news.html')


@login_required
@user_passes_test(is_admin)
def survey_report(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = SurveyResponse.objects.filter(survey=survey).select_related('user')
    
    # Process responses to include repeater sub-answers
    processed_responses = []
    for resp in responses:
        if isinstance(resp.answers, dict):
            new_answers = {}
            for key, value in resp.answers.items():
                new_answers[str(key)] = value
            
            # Process repeater answers into a list format for easier template rendering
            repeater_data = {}
            for q in survey.questions:
                if q.get('type') == 'repeater':
                    q_id = str(q['id'])
                    source_id = str(q.get('repeat_source'))
                    member_count = int(new_answers.get(source_id, 0) or 0)
                    if member_count > 0 and q.get('sub_questions'):
                        repeater_data[q_id] = []
                        for member_idx in range(member_count):
                            member_data = {
                                'member_number': member_idx + 1,
                                'answers': []
                            }
                            for sub_idx, sub_q in enumerate(q['sub_questions']):
                                sub_key = f"r{q['id']}_{member_idx}_{sub_idx}"
                                answer_value = new_answers.get(sub_key, '')
                                # Handle arrays (for checkboxes)
                                if isinstance(answer_value, list):
                                    answer_value = ', '.join(str(v) for v in answer_value)
                                member_data['answers'].append({
                                    'question': sub_q.get('text', f'Sub-Q{sub_idx+1}'),
                                    'answer': str(answer_value) if answer_value else '(No answer)'
                                })
                            repeater_data[q_id].append(member_data)
            
            processed_responses.append({
                'user': resp.user.username,
                'submitted_at': resp.submitted_at,
                'answers': new_answers,
                'repeater_data': repeater_data
            })
    
    context = {
        'survey': survey,
        'responses': processed_responses,
    }
    return render(request, 'survey_report.html', context)


@login_required
@user_passes_test(is_admin)
def export_responses(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = SurveyResponse.objects.filter(survey=survey).select_related('user')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{survey.title}_responses.csv"'
    
    writer = csv.writer(response)
    
    # Header row
    header = ['User', 'Date Submitted']
    for q in survey.questions:
        if q['type'] == 'standard':
            header.append(q['text'])
        elif q['type'] == 'repeater':
            header.append(f"{q['repeat_label']} Count")
            # Add columns for each sub-question
            if q.get('sub_questions'):
                for sub_q in q['sub_questions']:
                    header.append(f"{q['repeat_label']} - {sub_q.get('text', 'Sub-Q')}")
    
    writer.writerow(header)
    
    for resp in responses:
        if isinstance(resp.answers, dict):
            new_answers = {}
            for key, value in resp.answers.items():
                new_answers[str(key)] = value
            
            row = [resp.user.username, resp.submitted_at.strftime("%Y-%m-%d %H:%M")]
            for q in survey.questions:
                q_id = str(q['id'])
                if q['type'] == 'standard':
                    row.append(new_answers.get(q_id, ''))
                elif q['type'] == 'repeater':
                    source_id = str(q.get('repeat_source'))
                    member_count = int(new_answers.get(source_id, 0) or 0)
                    row.append(member_count)
                    # Add sub-question answers for each member
                    if q.get('sub_questions'):
                        for member_idx in range(member_count):
                            for sub_idx, sub_q in enumerate(q['sub_questions']):
                                sub_key = f"r{q['id']}_{member_idx}_{sub_idx}"
                                answer = new_answers.get(sub_key, '')
                                # Handle arrays (for checkboxes)
                                if isinstance(answer, list):
                                    answer = ', '.join(str(v) for v in answer)
                                row.append(str(answer))
            writer.writerow(row)
        
    return response


@login_required
@user_passes_test(is_admin)
def reset_survey(request, survey_id):
    """Clear all responses for a survey so it can be taken again from scratch."""
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        SurveyResponse.objects.filter(survey=survey).delete()
        messages.success(request, f'All responses for \"{survey.title}\" have been cleared.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def delete_survey(request, survey_id):
    """Permanently delete a survey and all its responses."""
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        survey.delete()
        messages.success(request, 'Survey deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

