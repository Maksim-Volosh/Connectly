from django.core.cache import cache
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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
        cache_key = f"profile:{pk}"
        data = cache.get(cache_key)
        
        if not data:
            try:
                profile = Profile.objects.get(pk=pk)
            except Profile.DoesNotExist:
                return Response(status=404)
            
            serializer = ProfileSerializer(profile)
            data = serializer.data
            cache.set(cache_key, data, timeout=30)
            
        return Response(data)