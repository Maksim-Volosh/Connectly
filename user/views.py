from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.services.profile import get_cached_profile

from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, pk=None):
        data = get_cached_profile(pk)
            
        return Response(data, status=status.HTTP_200_OK) if data else Response(status=status.HTTP_404_NOT_FOUND)