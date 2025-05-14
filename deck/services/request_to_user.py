import random

from user.models import Profile
from user.services.profile import (get_profiles_by_filters,
                                        serialize_profiles)


def request_to_get_profiles_by_filters(telegram_id, city, age__in, prefer_gender__in, gender={}):
    return get_profiles_by_filters(telegram_id, city, age__in, prefer_gender__in, gender=gender)

def request_to_get_serialized_profiles(profiles):
    return serialize_profiles(profiles)