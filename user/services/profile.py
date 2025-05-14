from user.models import Photo, Profile
import random


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