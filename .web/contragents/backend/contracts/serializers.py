from rest_framework import serializers
from contracts import models


class ContractSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source="agent.title", read_only=True)

    class Meta:
        model = models.Contract
        fields = [
            "id",
            "agent_id",
            "agent_name",
            "total",
            "date",
            "comment_id",
            "file",
        ]
