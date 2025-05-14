from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from deck.services.build_deck import DeckBuilderService
from user.models import Profile

class GetNextProfile(APIView):
    def get(self, request, telegram_id):
        profile = 0
        try:
            profile = DeckBuilderService.next_profile(telegram_id=telegram_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile with this telegram_id does not exist'})
        
        return Response(profile, status=status.HTTP_200_OK)