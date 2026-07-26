from memory.episode import Episode
from memory.memory_retriever import MemoryRetriever

episode = Episode(

    episode_id="query",

    start_time="13:00",

    end_time="14:00",

    trigger="Comfort",

    summary="Comfort degraded during afternoon occupancy.",

    average_outdoor_temp=31,

    average_building_power=18100,

    average_hvac_power=5100,

    average_comfort=88,

    worst_zone="CORE_TOP",

    actions=[],

    outcome=""

)

retriever = MemoryRetriever()

episodes = retriever.retrieve(

    episode

)

print("\nRetrieved Episodes\n")

for ep in episodes:

    print("--------------------------------")

    print(ep["id"])

    print(ep["distance"])

    print(ep["metadata"])

    print(ep["document"])