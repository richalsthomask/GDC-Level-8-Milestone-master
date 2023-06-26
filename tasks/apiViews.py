from rest_framework.serializers import ModelSerializer
from tasks.models import Task, TaskHistory, STATUS_CHOICES_HISTORY
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    ChoiceFilter,
    DateTimeFilter,
)
from tasks.models import STATUS_CHOICES
from django import forms


class userSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskSerializer(ModelSerializer):
    user = userSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "created_date",
            "user",
            "priority",
        ]


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskHistoryFilter(FilterSet):
    old_status = ChoiceFilter(choices=STATUS_CHOICES_HISTORY)
    new_status = ChoiceFilter(choices=STATUS_CHOICES_HISTORY)
    changed_date = DateTimeFilter(
        field_name="changed_date",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        ),
        lookup_expr="gt",
        label="Changed Date",
    )


class TaskHistorySerializer(ModelSerializer):
    user = userSerializer(read_only=True)

    class Meta:
        model = TaskHistory
        fields = [
            "task",
            "old_status",
            "new_status",
            "changed_date",
            "user",
        ]


class TaskHistoryViewSet(ModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskHistoryFilter

    def get_queryset(self):
        return TaskHistory.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
