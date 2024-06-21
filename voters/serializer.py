from rest_framework import serializers
from .models import Election, Campus,Candidate, Vote, Message


class ElectionGetSerializer(serializers. ModelSerializer):
    class Meta:
        model = Election
        fields = "__all__"
        depth = 2


class ElectionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = [ 'campus', 'election_date', 'election_time', 'active_election']


class CampusGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = "__all__"
        depth = 2


class CampusPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'user', 'campus_name', 'campus_location']


class VoteGetSerializer(serializers. ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        depth = 2


class VotePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'campus', 'candidate', 'election', 'no_votes', 'votes_ranking']


class MessageGetSerializer(serializers. ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        depth = 2


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'message_description']


class CandidateGetSerializer(serializers. ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        depth = 2


class CandidatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'user', 'campus', 'candidate_position','candidate_doc','candidate_description']