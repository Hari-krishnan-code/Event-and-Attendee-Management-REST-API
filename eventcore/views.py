from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from eventcore.serializers import RegisterSerializer, EventSerializer, EventAttendeeSerializer
from eventcore.models import EventDb, EventAttendeeDb
from eventcore.permissions import OwnerOnly

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer_instance = RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message": "User registered successfully!"})
        return Response({
            "message": "Invalid data provided!",
            "errors": serializer_instance.errors
            })

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer_instance = RegisterSerializer(users, many=True)
        return Response(serializer_instance.data)

class EventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = EventDb.objects.filter(created_by=request.user)
        serializer_instance = EventSerializer(qs, many=True)
        return Response(data=serializer_instance.data)

    def post(self, request):
        form_data = request.data
        serializer_instance = EventSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "Message": "Event Created Successfully!",
                "Event Details": serializer_instance.data
            })
        return Response(data=serializer_instance.errors)

class EventRetrieveUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]
    def get(self, request, pk):
        event_object = get_object_or_404(EventDb, id=pk)
        if event_object.created_by == request.user:
            serializer_instance = EventSerializer(event_object)
            return Response(data=serializer_instance.data)
        raise serializers.ValidationError("YOU SHALL NOT PASS!")

    def put(self, request, pk):
        event_object = get_object_or_404(EventDb, id=pk)
        if event_object.created_by != request.user:
            raise serializers.ValidationError("YOU SHALL NOT PASS!")
        form_data = request.data
        serializer_instance = EventSerializer(data=form_data, instance=event_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message": "Event details updated!",
                "Updated details": serializer_instance.data
            })
        return Response(data=serializer_instance.errors)

    def delete(self, request, pk):
        event_object = get_object_or_404(EventDb, id=pk)
        if event_object.created_by == request.user:
            event_object.delete()
            return Response(data={"Message": "Event deleted!"})
        return Response({"Message": "You dont have access"})

class EventAttendeeListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, event_id):
        event_object = get_object_or_404(EventDb, id=event_id)
        is_owner = event_object.created_by == request.user
        is_attendee = EventAttendeeDb.objects.filter(event=event_object, user=request.user).exists()
        if not (is_owner or is_attendee):
            raise PermissionDenied("YOU SHALL NOT PASS!")
        attendees = EventAttendeeDb.objects.filter(event=event_object)
        serializer_instance = EventAttendeeSerializer(attendees, many=True)
        return Response(data=serializer_instance.data)

    def post(self, request, event_id):
        event_object = get_object_or_404(EventDb, id=event_id)
        if event_object.created_by != request.user:
            raise PermissionDenied("Only event owner can add attendees!")
        form_data = request.data
        serializer_instance = EventAttendeeSerializer(data=form_data, context={'event': event_object})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"Message": "Event attendee added successfully!"})
        return Response(data=serializer_instance.errors)

class AttendeeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, event_id, attendee_id):
        event_object = get_object_or_404(EventDb, id=event_id)
        if event_object.created_by != request.user:
            raise PermissionDenied("Only the event owner can remove attendees!")
        attendee_object = get_object_or_404(EventAttendeeDb, id=attendee_id, event=event_object)
        attendee_object.delete()
        return Response(data={"Message": "Attendee deleted successfully!"})

class JWT_logout(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Message": "Logout successful!"})
        except Exception:
            return Response({"Error": "Invalid refresh token!"})