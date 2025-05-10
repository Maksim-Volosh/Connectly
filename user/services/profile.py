from ..models import Photo, Profile


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