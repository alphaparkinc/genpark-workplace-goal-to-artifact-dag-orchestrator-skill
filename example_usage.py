"""Example usage for WorkplaceGoalToArtifactDAGOrchestrator."""
import json
from client import WorkplaceGoalToArtifactDAGOrchestrator

def main():
    print("=== Workplace Goal-to-Artifact Orchestrator Demo ===")
    orch = WorkplaceGoalToArtifactDAGOrchestrator()
    
    goal = "FY2026 Enterprise SaaS Expansion & Competitor Triage"
    
    # 1. Decompose to DAG
    dag = orch.decompose_goal_to_dag(goal)
    print("Task Execution DAG:", json.dumps(dag, indent=2))
    
    # 2. Deliver complete bundle
    bundle = orch.deliver_executive_artifact_bundle(goal)
    print("\nDelivered Executive Bundle Summary:")
    print(" - Bundle ID:", bundle["bundle_id"])
    print(" - Spreadsheet Rows:", bundle["deliverables"]["spreadsheet_model"]["row_count"])
    print(" - Presentation Slides:", bundle["deliverables"]["presentation_deck"]["slide_count"])

if __name__ == "__main__":
    main()
