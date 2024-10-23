from django.urls import path
from .views import PlacementScheduleView,BatchStatisticsView


urlpatterns = [
    path('placement/', PlacementScheduleView.as_view(), name='placement-list'),
    path('placement/<int:id>/', PlacementScheduleView.as_view(), name='placement-list'),
    path('statistics/',BatchStatisticsView.as_view()),
]