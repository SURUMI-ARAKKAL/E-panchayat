from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('create-survey/', views.create_survey, name='create_survey'),
    path('survey/<int:survey_id>/', views.view_survey, name='view_survey'),
    path('survey/<int:survey_id>/submit/', views.submit_survey, name='submit_survey'),
    path('survey/<int:survey_id>/responses/', views.survey_responses, name='survey_responses'),
    path('survey/<int:survey_id>/report/', views.survey_report, name='survey_report'),
    path('survey/<int:survey_id>/export/', views.export_responses, name='export_responses'),
    path('survey/<int:survey_id>/reset/', views.reset_survey, name='reset_survey'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
    path('add-user/', views.add_user, name='add_user'),
    path('add-news/', views.add_news, name='add_news'),
]

