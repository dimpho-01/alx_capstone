from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrSelf
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class TaskFilter(filters.FilterSet):
    """
    FilterSet for the Task model to allow filtering tasks by certain parameters.
    """

    due_date_gte = filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date_lte = filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    due_date = filters.DateTimeFilter(lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date', 'due_date_gte', 'due_date_lte']

class TaskListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating tasks.
    
    This view ensures that only authenticated users can list and create tasks.
    Tasks are filtered to only include those owned by the requesting user,
    applying the defined filters and ordering by specified fields.
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['due_date', 'priority']
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Return a queryset that lists tasks owned by the requesting user.
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    # Save the newly created task, assigning the current user as its owner.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)













class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting tasks.
    
    Only allows operations on tasks owned by the requesting user.
    Editing a completed task is prohibited unless its status is being reverted to pending.
    """
     
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Return a queryset that includes only tasks owned by the requesting user.
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    # Handle task updates, enforcing the rule that completed tasks cannot be edited.
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status == 'COMPLETED' and ('status' not in request.data or request.data['status'] == 'COMPLETED'):
            return Response({'detail': "Completed tasks cannot be edited unless reverted to 'Pending' status."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
    
class UserListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all user accounts and creating new user accounts.
    
    Restricted to admin users for listing all users.
    Authenticated users can still create new accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [IsAdminUser]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting user information.
    
    Restricted so that admin users can access any user's information, while regular users
    can only access their own information.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing tasks.
    
    Provides custom actions to mark tasks as complete or incomplete.
    Ensures users can only access and modify their own tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Filters the queryset to only include tasks owned by the requesting user.
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # Sets the correct user for the task when creating it.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom action to mark the specified task as complete.
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None, *args, **kwargs):
        task = self.get_object()
        if task.status == 'COMPLETED':
            return Response({'status': 'Task is already completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = 'COMPLETED'
        task.save()
        return Response({'status': 'Task marked as complete'}, status=status.HTTP_200_OK)

    # Custom action to mark the specified task as incomplete.
    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None, *args, **kwargs):
        task = self.get_object()
        task.status = 'PENDING'
        task.save()
        return Response({'status': 'Task marked as incomplete'}, status=status.HTTP_200_OK)
    