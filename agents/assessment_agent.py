"""
assessment_agent.py

Creates an overall assessment of the building.
"""


class AssessmentAgent:

    def __init__(self):
        pass

    def assess(self, building_state, metrics_report):

        zone_reports = metrics_report["zones"]
        summary = metrics_report["summary"]
        energy = metrics_report["energy"]
        carbon = metrics_report["carbon"]

        comfortable = 0
        uncomfortable = 0

        for zone_name, zone_data in zone_reports.items():

            comfort = zone_data["comfort"]

            if abs(comfort["pmv"]) <= 0.5:
                comfortable += 1
            else:
                uncomfortable += 1

        if uncomfortable == 0:
            overall = "Healthy"
        elif uncomfortable <= 2:
            overall = "Needs Minor Attention"
        else:
            overall = "Needs Immediate Attention"

        return {

            "overall_health": overall,

            "comfortable_zones": comfortable,

            "uncomfortable_zones": uncomfortable,

            "total_zones": len(zone_reports),

            "average_comfort": summary["average_comfort"],

            "worst_zone": summary["worst_zone"],

            "energy_status": energy["status"],

            "carbon_status": carbon["status"]

        }