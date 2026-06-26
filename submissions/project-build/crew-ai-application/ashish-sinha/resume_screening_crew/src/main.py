import argparse
import sys
import os
import json
from rich.console import Console
from crew import ResumeScreeningCrew
from output_writer import OutputWriter

console = Console()

def run_pipeline():
    parser = argparse.ArgumentParser(description="AI Resume Screening Crew Platform CLI")
    parser.add_argument("--candidate-id", type=str, help="Run target pipeline evaluation for single ID input.")
    parser.add_argument("--run-sample-screening", action="store_true", help="Batch execute criteria for MANDATORY profiles: CAND-001, CAND-002, CAND-003.")
    
    args = parser.parse_args()
    
    if not args.candidate_id and not args.run_sample_screening:
        parser.print_help()
        sys.exit(1)
        
    crew_pipeline = ResumeScreeningCrew()
    writer = OutputWriter(output_dir="outputs")
    
    if args.candidate_id:
        console.print(f"Starting orchestration flow targeting input: {args.candidate_id}...")
        try:
            res = crew_pipeline.kickoff(candidate_id=args.candidate_id)
            writer.write_json_report(candidate_id=args.candidate_id, report_data=res)
            console.print(f"Pipeline completed! Recommendation: {res.get('recommendation')}")
        except Exception as e:
            # FIX: Cleaned string printing to prevent rich markup errors
            console.print(f"[bold red]Execution error occurred:[/bold red] {str(e)}")
            
            # CRITICAL FALLBACK: Ensure an error snapshot JSON file is written to the outputs folder
            fallback_data = {
                "status": "PIPELINE_CRASHED_OR_RATE_LIMITED",
                "candidate_id": args.candidate_id,
                "error_message": str(e),
                "recommendation": "NEEDS_MANUAL_REVIEW"
            }
            writer.write_json_report(candidate_id=args.candidate_id, report_data=fallback_data)
            
    elif args.run_sample_screening:
        mandatory_targets = ["CAND-001", "CAND-002", "CAND-003"]
        console.print(f"Executing target system batch processing for: {mandatory_targets}")
        for cid in mandatory_targets:
            console.print(f"\n--- Processing Session ID: {cid} ---")
            try:
                res = crew_pipeline.kickoff(candidate_id=cid)
                writer.write_json_report(candidate_id=cid, report_data=res)
                console.print(f"Successfully saved assessment data for target {cid}. Band: {res.get('recommendation')}")
            except Exception as e:
                console.print(f"[bold red]Failed processing profile metrics for target {cid}:[/bold red] {str(e)}")
                fallback_data = {
                    "status": "BATCH_PIPELINE_CRASHED_OR_RATE_LIMITED",
                    "candidate_id": cid,
                    "error_message": str(e),
                    "recommendation": "NEEDS_MANUAL_REVIEW"
                }
                writer.write_json_report(candidate_id=cid, report_data=fallback_data)

if __name__ == "__main__":
    run_pipeline()
