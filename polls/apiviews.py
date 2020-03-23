from django.contrib.auth import authenticate
from rest_framework import (
							generics,
							views,
							response,
							status,
							viewsets,
							exceptions,
							)

from .models import Poll, Choice
from .serializers import (
							PollSerializer, 
							ChoiceSerializer,
							VoteSerializer,
							UserSerializer,
							)

class PollViewSet(viewsets.ModelViewSet):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

	def create(self, request):
		user_pk = request.user.pk
		question = request.data.get("question")
		data = {'question': question, 'created_by': user_pk}
		serializer = PollSerializer(data=data)
		if serializer.is_valid():
			choice = serializer.save()
			return response.Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs["pk"])
		if not request.user == poll.created_by:
			raise exceptions.PermissionDenied("You can not delete this poll.")
		return super().destroy(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs["pk"])
		if not request.user == poll.created_by:
			raise exceptions.PermissionDenied("You can not update this poll.")
		request.POST._mutable = True
		request.POST['created_by'] = request.user.pk
		request.POST._mutable = False
		return super().update(request, *args, **kwargs)

class ChoiceList(generics.ListCreateAPIView):
	serializer_class = ChoiceSerializer

	def get_queryset(self):
		queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
		return queryset

	def post(self, request, pk):
		poll = Poll.objects.get(pk=pk)
		if not request.user == poll.created_by:
			raise exceptions.PermissionDenied("You can not create choice for this poll.")
		choice_text = request.data.get("choice_text")
		data = {'choice_text': choice_text, 'poll':pk}
		serializer = ChoiceSerializer(data=data)
		if serializer.is_valid():
			choice = serializer.save()
			return response.Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateVote(views.APIView):
	serializer_class = VoteSerializer

	def post(self, request, pk, choice_pk):
		voted_by = request.data.get("voted_by")
		data = {'choice': choice_pk, 'poll': pk, 'voted_by': request.user.pk}
		serializer = VoteSerializer(data=data)
		if serializer.is_valid():
			vote = serializer.save()
			return response.Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
