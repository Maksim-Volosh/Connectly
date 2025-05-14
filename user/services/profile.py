import random

from django.core.cache import cache
from rest_framework.response import Response

from user.models import Photo, Profile
from user.serializers import ProfileSerializer


def create_profile_with_photos(validated_data):
    photos_data = validated_data.pop('photos', [])
        
    profile = Profile.objects.create(**validated_data)
        
    photos = [Photo(profile=profile, photo=photo) for photo in photos_data]
    Photo.objects.bulk_create(photos)
    
    return profile

def update_profile_with_photos(instance, validated_data):
    photos_data = validated_data.pop('photos', [])
    
    for attr, value in validated_data.items():
        setattr(instance, attr, value) 
    instance.save()
    
    if photos_data:
        for photo in instance.photos.all():
            photo.photo.delete(save=False)
            photo.delete()
            
        photos = [Photo(profile=instance, photo=photo) for photo in photos_data]
        Photo.objects.bulk_create(photos)
        
    return instance

def serialize_profiles(profiles):
    from user.serializers import ProfileSerializer
    serialized = ProfileSerializer(profiles, many=True).data
    return serialized

def get_profiles_by_filters(telegram_id, city, age__in, prefer_gender__in, gender={}):
    if gender != {}:
        profiles = Profile.objects.filter(
            city=city, age__in=age__in, prefer_gender__in=prefer_gender__in, gender=gender).exclude(telegram_id=telegram_id)
    else:
        profiles = Profile.objects.filter(
            city=city, age__in=age__in, prefer_gender__in=prefer_gender__in).exclude(telegram_id=telegram_id)

    profiles = list(profiles)
    random.shuffle(profiles)
    
    return profiles 

def get_cached_profile(pk):
    cache_key = f"profile:{pk}"
    data = cache.get(cache_key)
    
    if not data:
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return None
        
        serializer = ProfileSerializer(profile)
        data = serializer.data
        cache.set(cache_key, data, timeout=30)
        
    return data refactor(ProfileViewSet): extract retrieve logic to get_cached_profile helper