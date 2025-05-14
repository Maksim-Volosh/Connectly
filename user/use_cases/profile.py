from user.services.profile import create_profile_with_photos
from user.services.request_to_deck import request_to_build_deck


def create_profile(validated_data):
    # Create profile with photos
    profile = create_profile_with_photos(validated_data)
    
    request_to_build_deck(profile.telegram_id)
    return profile
