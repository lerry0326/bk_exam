# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Task, TestCase, HostInfo


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = serializers.ALL_FIELDS


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = serializers.ALL_FIELDS


class HostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostInfo
        fields = serializers.ALL_FIELDS
