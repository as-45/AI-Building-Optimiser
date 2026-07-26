from memory.episode import Episode
from memory.embedding_model import EmbeddingModel

episode = Episode(

    episode_id="1",

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

model = EmbeddingModel()

embedding = model.embed(episode)

print("Embedding Dimension:", len(embedding))

print("First 10 Values:")

print(embedding[:10])