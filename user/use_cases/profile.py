from deck.services.build_deck import DeckBuilderService
from user.services.profile import create_profile_with_photos


def create_profile(validated_data):
    # Create profile with photos
    profile = create_profile_with_photos(validated_data)
    
    # Build deck for this profile
    telegram_id = profile.telegram_id
    DeckBuilderService.build_deck(telegram_id)
    
    return profile
