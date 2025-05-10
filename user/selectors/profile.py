from user.models import Profile


def is_profile_with_telegram_id_exists(telegram_id):
    return Profile.objects.filter(telegram_id=telegram_id).exists()
