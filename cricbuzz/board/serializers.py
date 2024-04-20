from rest_framework import serializers
from board.models import CustomUser,Player,Match,Team

class UserSerializer(serializers.ModelSerializer):
  password=serializers.CharField(write_only=True) 

  class Meta:
    model=CustomUser
    fields=['name','email','password']

  def create(self,validated_data):
    password=validated_data.pop('password',None)
    instance=super().create(validated_data)
    if password:
        instance.set_password(password)
        instance.save()
    return instance
  
  def update(self,instance,validated_data):
    password=validated_data.pop('password',None)
    instance=super().update(validated_data)
    if password:
        instance.set_password(password)
        instance.save() 
    return instance


class UserDetailSerializer(serializers.ModelSerializer):
  class Meta:
      model=CustomUser
      fields=['id','name','email']

class TeamSerializer(serializers.ModelSerializer):
   class Meta:
      model=Team
      fields='__all__'


class PlayerSerializer(serializers.ModelSerializer):
   team=TeamSerializer(read_only=True)
   class Meta:
      model=Player
      fields='__all__'


class MatchSerializer(serializers.ModelSerializer):
  #  team1=TeamSerializer()
  #  team2=TeamSerializer()
   team1=TeamSerializer(read_only=True)
   team2=TeamSerializer(read_only=True)

   class Meta:
      model=Match
      fields=['team1','team2','date','venue']
