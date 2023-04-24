from django.urls import path

from core.views.auth import LoginView
from core.views.course_material import CourseMaterialListView, CourseMaterialCreateView, CourseMaterialUpdateView, CourseMaterialV2CreateView
from core.views.dashboard import DashboardView
from core.views.exam import ExamListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('course_material/', CourseMaterialListView.as_view(), name='course_material'),
    path('course_material/create/', CourseMaterialCreateView.as_view(), name='course_material_create'),
    path('course_material/update/<int:pk>/', CourseMaterialUpdateView.as_view(), name='course_material_update'),
    path('', DashboardView.as_view(), name='home'),
    path('exam/', ExamListView.as_view(), name='exam'),
    path('course_material/create_v2/', CourseMaterialV2CreateView.as_view(), name='course_material_create_v2'),

]
