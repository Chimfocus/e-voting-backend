from django.urls import path
from .views import *

urlpatterns = [
    path('candidate/', CandidateView.as_view(), name='candidate'),
    path('election/', ElectionView.as_view(), name='election'),
    path('campus/', CampusView.as_view(), name='campus'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('message/', MessageView.as_view(), name='message'),
]
