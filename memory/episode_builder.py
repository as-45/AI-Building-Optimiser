"""
episode_builder.py

Builds episodes from the History Buffer.
"""

from memory.episode import Episode


class EpisodeBuilder:

    def __init__(self):

        pass

    def build(

        self,

        history,

        trigger

    ):

        """
        Later this function will convert
        the last hour of history into one episode.
        """

        return Episode(

            episode_id="",

            start_time="",

            end_time="",

            trigger=trigger,

            summary="",

            average_outdoor_temp=0,

            average_building_power=0,

            average_hvac_power=0,

            average_comfort=0,

            worst_zone="",

            actions=[],

            outcome=""

        )