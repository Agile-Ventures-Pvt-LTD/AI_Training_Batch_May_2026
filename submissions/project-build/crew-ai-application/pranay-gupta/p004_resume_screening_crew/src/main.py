import argparse
import sys
from pathlib import Path
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.crew import ResumeScreeningCrew
from src.output_writer import append_execution_log

console = Console()

def main():
    parser = argparse.ArgumentParser(description="P004 Resume Screening Crew")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--candidate-id", type=str)
    group.add_argument("--run-sample-screening", action="store_true")
    group.add_argument("--run-all", action="store_true")

    args = parser.parse_args()
    crew = ResumeScreeningCrew()
    
    append_execution_log("Session Started")

    if args.candidate_id:
        console.print(f"[cyan]Screening {args.candidate_id}...[/cyan]")
        crew.run(args.candidate_id)
        console.print(f"[green]Done.[/green]")
    elif args.run_sample_screening:
        console.print("[cyan]Running sample screening...[/cyan]")
        crew.run_sample_screening()
        console.print("[green]Done.[/green]")
    elif args.run_all:
        console.print("[cyan]Running all...[/cyan]")
        crew.run_batch(["CAND-001", "CAND-002", "CAND-003", "CAND-004", "CAND-005"])
        console.print("[green]Done.[/green]")

if __name__ == "__main__":
    main()