from django.urls import path
from .views import *


urlpatterns = [
    path('placement/', PlacementScheduleView.as_view(), name='placement-list'),
    path('placement/<int:id>/', PlacementScheduleView.as_view(), name='placement-list'),
    path('statistics/',BatchStatisticsView.as_view()),
    path('delete-statistics/<int:id>/',BatchStatisticsView.as_view()),
    path('generate-cv/',generate_cv,name='generate_cv'),
    path('apply-placement/',ApplyForPlacement.as_view(),name="apply"),
    path('student-applications/<int:id>/',ApplyForPlacement.as_view()),
    path('calender/',NextRoundDetails.as_view()),
    path('nextround/<int:id>/',NextRoundDetails.as_view()),
    path('timeline/<int:id>/',TrackStatus.as_view()),
    path('download-applications/<int:id>/',DownloadApplications.as_view()),
    path('download-statistics/',DownloadStatistics.as_view()),
]