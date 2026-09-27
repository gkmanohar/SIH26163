from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('attack-surface/', views.attack_surface, name='attack_surface'),
    path('ai-firewall/', views.ai_firewall, name='ai_firewall'),
    path('protocol-shield/', views.protocol_shield, name='protocol_shield'),
    path('desktop-guard/', views.desktop_guard, name='desktop_guard'),
    path('findings/', views.findings_list, name='findings_list'),
    path('findings/<str:finding_id>/', views.finding_detail, name='finding_detail'),
    path('evidence/', views.evidence_vault, name='evidence_vault'),
    path('fix-validation/', views.fix_validation, name='fix_validation'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_page, name='settings_page'),
]
