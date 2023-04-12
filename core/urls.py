from django.urls import path

from core.views.auth import LoginView
from core.views.course_material import CourseMaterialListView, CourseMaterialCreateView, CourseMaterialUpdateView
from core.views.dashboard import DashboardView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('course_material/', CourseMaterialListView.as_view(), name='course_material'),
    path('course_material/create/', CourseMaterialCreateView.as_view(), name='course_material_create'),
    path('course_material/update/<int:pk>/', CourseMaterialUpdateView.as_view(), name='course_material_update'),
    path('', DashboardView.as_view(), name='home'),

]