from django.urls import path
from .views import UserLogout,UserRegister,PlayerDetailView,MatchesView,MatchCreateView,AddPlayer,MatchView

urlpatterns = [
    path('api/register/',UserRegister.as_view(),name='register'),
    path('api/players/<int:pk>/stats',PlayerDetailView.as_view(),name='player_detail'),
    path('api/matches',MatchesView.as_view(),name='matches_list'),
    path('api/create-match/',MatchCreateView.as_view(),name='match_creation'),
    path('api/teams/<int:pk>/squad',AddPlayer.as_view(),name='player_add'),
    path('api/matches/<int:pk>',MatchView.as_view(),name='specific_match'),
]