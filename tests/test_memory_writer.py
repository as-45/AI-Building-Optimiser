from memory.episode import Episode
from memory.memory_writer import MemoryWriter

episode = Episode(

    episode_id="episode_001",

    start_time="09:00",

    end_time="10:00",

    trigger="Comfort",

    summary="Comfort degraded during increasing occupancy.",

    average_outdoor_temp=31.2,

    average_building_power=18000,

    average_hvac_power=5200,

    average_comfort=87,

    worst_zone="CORE_TOP",

    actions=["Reduce cooling setpoint by 1°C"],

    outcome="Comfort recovered while saving 8% HVAC energy."

)

writer = MemoryWriter()

writer.store(episode)