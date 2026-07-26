"""
episode_narrator.py

Turns a building Episode into a natural-language description for the
embedding model to encode. Field names here match memory.episode.Episode
exactly:
    episode_id, start_time, end_time, trigger, summary,
    average_outdoor_temp, average_building_power, average_hvac_power,
    average_comfort, worst_zone, actions, outcome
"""


class EpisodeNarrator:

    def narrate(self, episode):

        if episode.actions:
            actions_text = ", ".join(str(a) for a in episode.actions)
        else:
            actions_text = "none"

        text = f"""

Episode {episode.episode_id}

Time Window

{episode.start_time} to {episode.end_time}

Trigger

{episode.trigger}

Summary

{episode.summary}

Average Outdoor Temperature

{episode.average_outdoor_temp}

Average Comfort

{episode.average_comfort}

Worst Zone

{episode.worst_zone}

Average Building Power

{episode.average_building_power}

Average HVAC Power

{episode.average_hvac_power}

Actions Taken

{actions_text}

Outcome

{episode.outcome}

"""

        return text