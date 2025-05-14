import json

from django_redis import get_redis_connection

from deck.services.request_to_user import (request_to_get_profiles_by_filters,
                                           request_to_get_serialized_profiles)
from user.models import Profile


class DeckBuilderService:
    redis = get_redis_connection("default")
    
    @classmethod
    def build_deck(cls, telegram_id):
        profile = Profile.objects.get(telegram_id=telegram_id)
        
        profile_age = profile.age
        profile_gender = profile.gender
        profile_city = profile.city
        
        prefer_gender = profile.prefer_gender
        prefer_ages = list(range(profile_age - 2, profile_age + 3))
        
        if prefer_gender != 'anyone':
            print(prefer_gender, profile_gender)
            profiles = request_to_get_profiles_by_filters(telegram_id, city=profile_city, age__in=prefer_ages, gender=prefer_gender, prefer_gender__in=("anyone", profile_gender))
        else:
            profiles = request_to_get_profiles_by_filters(telegram_id, city=profile_city, age__in=prefer_ages, prefer_gender__in=("anyone", profile_gender))
        
        if profiles:
            serialized = request_to_get_serialized_profiles(profiles)
            deck_key = f"deck:{telegram_id}"
            
            cls.redis.delete(deck_key)  
            cls.redis.rpush(deck_key, *[json.dumps(p) for p in serialized])
            cls.redis.expire(deck_key, 60 * 60 * 12)
        

    @classmethod
    def next_profile(cls, telegram_id):
        deck_key = f"deck:{telegram_id}"

        raw = cls.redis.lpop(deck_key)

        if raw is None:
            cls.build_deck(telegram_id)
            raw = cls.redis.lpop(deck_key)

        return json.loads(raw) if raw else {'message': 'Not found'}