from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from board.serializers import UserDetailSerializer,UserSerializer,PlayerSerializer,MatchSerializer,TeamSerializer
from board.models import Player,CustomUser,Team,Match
from rest_framework import permissions
class UserRegister(APIView):
    permission_classes=[AllowAny]

    def post(self,request,format=None):
        serialized_data=UserSerializer(data=request.data)
        if serialized_data.is_valid():
            user=serialized_data.save()
            user.save()
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PlayerDetailView(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,pk,format=None):
        player=Player.objects.get(id=pk)
        return Response({
            "player_id":player.id,
            "name":player.name,
            "matches_played":player.matches_played,
            "runs":player.runs,
            "average":player.average,
            "strike_rate":player.strike_rate
        })

class MatchesView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        matchlist=[]
        matches=Match.objects.all()
        for match in matches:
            temp_obj={
                "match_id":match.id,
                "team_1":match.team1.name,
                "team_2":match.team2.name,
                "date":match.date,
                "venue":match.venue
            }
            matchlist.append(temp_obj)

        return Response({"matches":matchlist})

class MatchView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk,format=None):
        match=Match.objects.get(id=pk)


        team1=[]
        for player in Player.objects.all().filter(team=match.team1):
            temp_obj={
                "player_id":player.id,
                "name":player.name
            }
            team1.append(temp_obj)

        team2=[]
        for player in Player.objects.all().filter(team=match.team2):
            temp_obj={
                "player_id":player.id,
                "name":player.name
            }
            team2.append(temp_obj)

        structure={
            "match_id":match.id,
            "team_1":match.team1.name,
            "team_2":match.team2.name,
            "date":match.date,
            "venue":match.venue,
            "status":match.status,
            "squads":{
                "team_1":team1,
                "team_2":team2
                        }
                  }
        return Response({"Response Data":structure})


class IsSuperuserOnly(permissions.BasePermission):
  
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class MatchCreateView(APIView):
    permission_classes=[IsAuthenticated,IsSuperuserOnly]
    def post(self,request):
        team1_name=request.data.get('team1')
        team2_name=request.data.get('team2')
        event_date=request.data.get('date')
        event_venue=request.data.get('venue')

        team1, created1 = Team.objects.get_or_create(name=team1_name)
        team2, created2 = Team.objects.get_or_create(name=team2_name)


        if Match.objects.filter(
            team1=team1,  date=event_date
        ).exists() or Match.objects.filter(
            team2=team1,  date=event_date
        ).exists():
            return Response(
                {"error": "team1 have already a match on that day"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        if Match.objects.filter(team1=team2,  date=event_date).exists() or Match.objects.filter(team2=team2, date=event_date).exists():
            return Response(
                {"error": "team2 have already a match on that day"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MatchSerializer(data={'date':event_date,'venue':event_venue})

        if serializer.is_valid():
            serializer.validated_data['team1']=team1
            serializer.validated_data['team2']=team2
            serializer.save()
            return Response({"message":"Match created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddPlayer(APIView):
    permission_classes=[IsAuthenticated,IsSuperuserOnly]
    def post(self,request,pk):
        player_name=request.data.get('name')
        player_role=request.data.get('role')
        team_assigned, created = Team.objects.get_or_create(id=pk)

        if Player.objects.filter(name=player_name,team=team_assigned).exists():
            return Response({"error":"Player already on team"},staus=status.HTTP_400_BAD_REQUEST)
        
        serializer=PlayerSerializer(data={'name':player_name,'role':player_role})
        if serializer.is_valid():
            serializer.validated_data['team']=team_assigned
            serializer.save()
            return Response({
                "message":"Player added to squad successfully",
                "player_id":Player.objects.get(name=player_name).id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

