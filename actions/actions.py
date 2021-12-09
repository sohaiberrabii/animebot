from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

ANIME_GENRES_MAPPING = {
    "action": 1,
    "adventure": 2,
    "comedy": 4,
    "mystery": 7,
    "fantasy": 10,
    "romance": 22,
}


class ValidateAnimeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_anime_form"

    @staticmethod
    def anime_ratings() -> List[Text]:
        return ["g", "pg", "pg13", "r17"]

    def validate_anime_genre(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate `anime_genre` value.
        """

        if value.lower() in ANIME_GENRES_MAPPING.keys():
            return {"anime_genre": value.lower()}
        else:
            dispatcher.utter_message(
                text=f"Unknown genre, Please choose"
                     f" from {'/'.join(ANIME_GENRES_MAPPING.keys())}"
            )
            return {"anime_genre": None}

    def validate_anime_rating(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate `anime_rating` value.
        """

        if value.lower() in self.anime_ratings():
            return {"anime_rating": value.lower()}
        else:
            dispatcher.utter_message(
                text=f"Unknown rating, Please choose"
                     f" from {'/'.join(self.anime_ratings())}"
            )
            return {"anime_rating": None}

    def validate_by_popularity(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate `by_popularity` value.
        """

        if tracker.get_intent_of_latest_message() == "affirm":
            return {"by_popularity": True}
        elif tracker.get_intent_of_latest_message() == "deny":
            return {"by_popularity": False}
        else:
            dispatcher.utter_message(text="I didn't get that.")
            dispatcher.utter_message(response="utter_ask_by_popularity")
            return {"by_popularity": None}


class SearchAnimeAction(Action):
    base_url = "https://api.jikan.moe/v3/search/anime"
    n_results = 5

    def name(self) -> Text:
        return "action_search_anime"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[SlotSet]:

        # Prepare query to jikan api
        query = {
            'genre': ANIME_GENRES_MAPPING[tracker.get_slot("anime_genre")],
            'rated': tracker.get_slot("anime_rating"),
            'limit': self.n_results,
        }
        if tracker.get_slot("by_popularity"):
            query['order_by'] = 'members'
            query['sort'] = 'desc'

        # Call jikan api
        results = requests.get(self.base_url, params=query).json()['results']

        # Keep only title and score of anime
        anime = [{k: r[k] for k in {'title', 'score'}} for r in results]

        # Utter results
        description = "\n".join([ani['title'] for ani in anime])
        dispatcher.utter_message(text=f"Found anime:\n{description}")
        return [SlotSet("anime", anime)]
