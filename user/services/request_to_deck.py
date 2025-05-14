from deck.services.build_deck import DeckBuilderService

def request_to_build_deck(telegram_id):
    DeckBuilderService.build_deck(telegram_id)
    return