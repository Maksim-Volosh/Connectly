import json

from django_redis import get_redis_connection

from user.models import Profile
from user.serializers import ProfileSerializer


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
            profiles = Profile.objects.filter(city=profile_city, age__in=prefer_ages, gender=prefer_gender, prefer_gender__in=("anyone", profile_gender))
        else:
            profiles = Profile.objects.filter(city=profile_city, age__in=prefer_ages, prefer_gender__in=("anyone", profile_gender))
            
        serialized = ProfileSerializer(profiles, many=True).data
        deck_key = f"deck:{telegram_id}"
        
        if serialized:
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

        return json.loads(raw) if raw else None