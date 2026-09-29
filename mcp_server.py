"""MCP JSON-RPC stdio server for genpark-workplace-goal-to-artifact-dag-orchestrator-skill."""
import sys
import json
from client import WorkplaceGoalToArtifactDAGOrchestrator

orchestrator = WorkplaceGoalToArtifactDAGOrchestrator()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "orchestrate_workplace_artifacts":
        return {"error": f"Unknown tool '{name}'"}
        
    action = args.get("action")
    goal = args.get("goal_title", "Q3 Strategy Deliverables")
    
    if action == "decompose_goal_to_dag":
        return orchestrator.decompose_goal_to_dag(goal)
    elif action == "compile_spreadsheet_model":
        return orchestrator.compile_spreadsheet_model(goal)
    elif action == "compile_presentation_deck":
        return orchestrator.compile_presentation_deck(goal)
    elif action == "deliver_executive_artifact_bundle":
        return orchestrator.deliver_executive_artifact_bundle(goal)
    else:
        return {"error": f"Unknown action '{action}'"}

def main():
    if "--test" in sys.argv:
        print("[TEST] Running self-test for WorkplaceGoalToArtifactDAGOrchestrator...")
        dag = orchestrator.decompose_goal_to_dag("Annual Cloud Budget Review")
        assert dag["task_count"] >= 3
        
        bundle = orchestrator.deliver_executive_artifact_bundle("Q4 Growth Review")
        assert bundle["status"] == "success"
        assert "presentation_deck" in bundle["deliverables"]
        print(f"[TEST] Success! Delivered Bundle: {bundle['bundle_id']}")
        return

    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "orchestrate_workplace_artifacts",
                                "description": "Decompose enterprise goals into multi-agent DAGs, synthesize spreadsheets, generate executive presentation slide decks, and bundle final deliverables.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "action": {"type": "string", "enum": ["decompose_goal_to_dag", "compile_spreadsheet_model", "compile_presentation_deck", "deliver_executive_artifact_bundle"]},
                                        "goal_title": {"type": "string"}
                                    },
                                    "required": ["action"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
