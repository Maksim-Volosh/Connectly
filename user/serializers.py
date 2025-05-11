from rest_framework import serializers


from .models import Photo, Profile
from .selectors.profile import is_profile_with_telegram_id_exists
from .services.profile import (create_profile_with_photos,
                               update_profile_with_photos)


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)

class ProfileSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    uploaded_photos = PhotoSerializer(source='photos', many=True, read_only=True)
    
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True, default='')
    
    def validate_photos(self, value):
        if self.instance is None and not value:
            raise serializers.ValidationError({"photos": 'At least one photo is required'})
        if len(value) > 3:
            raise serializers.ValidationError({"photos": 'Too many photos'})
        return value
    
    def create(self, validated_data):
        return create_profile_with_photos(validated_data)
    
    def update(self, instance, validated_data):
        return update_profile_with_photos(instance, validated_data)


    class Meta: 
        model = Profile
        fields = (
            'telegram_id', 'name', 'age', 'city',
            'description', 'gender', 'prefer_gender',
            'photos', 'uploaded_photos'
        )