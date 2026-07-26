from llm.context_formatter import ContextFormatter

from llm.sections.mission import MissionSection
from llm.sections.trigger import TriggerSection
from llm.sections.building import BuildingSection
from llm.sections.zones import ZoneSection

from llm.sections.energy import EnergySection
from llm.sections.carbon import CarbonSection
from llm.sections.trends import TrendSection
from llm.sections.memory import MemorySection
from llm.sections.weather import WeatherSection
from llm.sections.objectives import ObjectivesSection
from llm.sections.constraints import ConstraintsSection
from llm.sections.actions import ActionsSection
from llm.sections.output_format import OutputFormatSection


class PromptBuilder:

    def __init__(self):

        self.formatter = ContextFormatter()

        self.sections = [

            MissionSection(),

            TriggerSection(),

            BuildingSection(),

            ZoneSection(),

            EnergySection(),

            CarbonSection(),

            TrendSection(),

            MemorySection(),

            WeatherSection(),

            ObjectivesSection(),

            ConstraintsSection(),

            ActionsSection(),

            OutputFormatSection()

        ]

    # ---------------------------------------------

    def build(self, context):

        prompt_sections = []

        for section in self.sections:

            prompt_sections.append(

                section.build(context)

            )

        return self.formatter.format(

            prompt_sections

        )