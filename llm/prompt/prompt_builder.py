from llm.prompt.context_formatter import ContextFormatter

from llm.prompt.sections.mission import MissionSection
from llm.prompt.sections.trigger import TriggerSection
from llm.prompt.sections.building import BuildingSection
from llm.prompt.sections.zones import ZoneSection

from llm.prompt.sections.energy import EnergySection
from llm.prompt.sections.carbon import CarbonSection
from llm.prompt.sections.trends import TrendSection
from llm.prompt.sections.memory import MemorySection
from llm.prompt.sections.weather import WeatherSection
from llm.prompt.sections.objectives import ObjectivesSection
from llm.prompt.sections.constraints import ConstraintsSection

from llm.prompt.actions import ActionsSection

from llm.prompt.sections.output_format import OutputFormatSection

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