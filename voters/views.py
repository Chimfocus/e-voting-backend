from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializer import *
from usermanagement.models import Campus


class CampusView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = CampusPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Campus.objects.all()
            serialized = CampusGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            campusId = request.GET.get("campusId")
            queryset = Campus.objects.get(id=campusId)
            serialized = CampusGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class CandidateView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        serialized = CandidatePostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Candidate.objects.all()
            serialized = CandidateGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            candidateId = request.GET.get("candidateId")
            queryset = Candidate.objects.get(id=candidateId)
            serialized = CandidateGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        elif querytype == "single_election":
            electionId = request.GET.get("electionId")
            queryset = Candidate.objects.filter(election=electionId)
            serialized = CandidateGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        serialized = VotePostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Vote.objects.all()
            serialized = VoteGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            voteId = request.GET.get("voteId")
            queryset = Vote.objects.get(id=voteId)
            serialized = VoteGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        serialized = MessagePostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Message.objects.all()
            serialized = MessageGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            messageId = request.GET.get("messageId")
            queryset = Message.objects.get(id=messageId)
            serialized = MessageGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class ElectionView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        serialized = ElectionPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Election.objects.all()
            serialized = ElectionGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            electionId = request.GET.get("electionId")
            queryset = Election.objects.get(id=electionId)
            serialized = ElectionGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})
