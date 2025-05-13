from rest_framework import serializers

from user.use_cases.profile import create_profile

from .models import Photo, Profile
from .services.profile import update_profile_with_photos


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)

class ProfileSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    uploaded_photos = PhotoSerializer(source='photos', many=True, read_only=True)
    
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True, default='')
    
    def validate_photos(self, value):
        if len(value) > 3:
            raise serializers.ValidationError({"photos": 'Too many photos'})
        return value
    
    def create(self, validated_data):
        photos = validated_data.get('photos', [])
        if not photos:
            raise serializers.ValidationError({"photos": 'At least one photo is required'})
        return create_profile(validated_data)
    
    def update(self, instance, validated_data):
        return update_profile_with_photos(instance, validated_data)


    class Meta: 
        model = Profile
        fields = (
            'telegram_id', 'name', 'age', 'city',
            'description', 'gender', 'prefer_gender',
            'photos', 'uploaded_photos'
        )