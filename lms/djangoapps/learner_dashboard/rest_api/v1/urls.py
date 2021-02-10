"""
URLs for the V1 of the Learner Dashboard API.
"""

from .views import ProgramDetailView, ProgramListView
from django.conf.urls import url

app_name = 'v1'
urlpatterns = [
    url(
        r'^programs/$',
        ProgramListView.as_view(),
        name='program_listing'
    ),
    url(
        r'^programs/(?P<program_uuid>[0-9a-f-]+)/$',
        ProgramDetailView.as_view(),
        name='program_details'
    ),
]
