from django.contrib.auth.models import User
from rest_framework import serializers
from eventcore.models import EventDb, EventAttendeeDb

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDb
        fields = "__all__"
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class EventAttendeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    attendee_username = serializers.CharField(source='user.username', read_only=True)
    attendee_user_id = serializers.IntegerField(source='user.id', read_only=True)
    class Meta:
        model = EventAttendeeDb
        fields = ["id", "username", "attendee_username", "attendee_user_id", "joined_at"]
        read_only_fields = ["id", "joined_at"]

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("This user is not registered!")

        event = self.context['event']
        if user == event.created_by:
            raise serializers.ValidationError("The creator is already the event owner!")
        if EventAttendeeDb.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("This user is already an attendee!")
        return value

    def create(self, validated_data):
        username = validated_data.pop("username")
        user = User.objects.get(username=username)
        event = self.context["event"]
        return EventAttendeeDb.objects.create(event=event, user=user)