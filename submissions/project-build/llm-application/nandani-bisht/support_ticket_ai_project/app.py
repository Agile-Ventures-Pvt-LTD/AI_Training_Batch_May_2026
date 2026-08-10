import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from config import load_config
from groq_client import call_groq_model
from output_parser import parse_json_response
from prompts import (
    build_classification_prompt,
    build_draft_response_prompt,
    build_priority_risk_prompt,
    build_quality_review_prompt,
    build_routing_prompt,
    build_sensitive_info_prompt,
    build_sentiment_prompt,
    build_summary_prompt,
)
from validators import validate_ticket_input


DEFAULT_OUTPUT_PATH = Path('outputs/sample_ticket_output.json')
SAMPLE_TICKET_INPUT = {
    'customer_name': 'Amit',
    'customer_type': 'Premium',
    'ticket_subject': 'Charged twice and no response from support',
    'ticket_body': (
        'Hi team, I cancelled my premium subscription last month, but I was still charged again this month. '
        'I also noticed that the same invoice amount appears twice on my bank statement. I contacted support two times '
        'last week but have not received any proper response. This is extremely frustrating. If this is not resolved '
        'today, I will escalate this publicly on LinkedIn and also ask our finance team to block future payments. '
        'Please refund the incorrect charge immediately. Regards, Amit'
    ),
    'product_area': 'Billing and subscription',
    'previous_interaction_history': (
        'Customer says they contacted support two times last week and did not receive a proper response.'
    ),
    'sla_tier': 'Premium',
    'response_tone': 'Professional and empathetic',
    'business_rules': [
        'Do not promise refund before verification.',
        'Do not confirm cancellation unless verified.',
        'Ask for invoice ID or registered account email if required.',
        'Escalate premium customer billing issues to billing support.',
    ],
}


def load_ticket_from_file(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def _run_prompt_with_repair(prompt: str, temperature: float, max_tokens: int) -> dict:
    raw_response = call_groq_model(prompt, temperature=temperature, max_tokens=max_tokens)
    try:
        return parse_json_response(raw_response)
    except ValueError:
        repair_prompt = (
            prompt
            + 'The previous response may have included extra text or formatting. Return valid JSON only matching the schema above.'
        )
        raw_retry = call_groq_model(repair_prompt, temperature=temperature, max_tokens=max_tokens)
        return parse_json_response(raw_retry)


def _build_section(prompt_builder, ticket, **kwargs):
    prompt = prompt_builder(ticket, **kwargs) if kwargs else prompt_builder(ticket)
    return _run_prompt_with_repair(prompt, temperature=0.2, max_tokens=900)


def run_ticket_analysis(ticket: dict) -> dict:
    ticket = {k: v for k, v in ticket.items() if v is not None}
    errors = validate_ticket_input(ticket)
    if errors:
        raise ValueError('Validation failed: ' + '; '.join(errors))

    summary = _build_section(build_summary_prompt, ticket)
    classification = _build_section(build_classification_prompt, ticket)
    sentiment = _build_section(build_sentiment_prompt, ticket)
    priority_and_risk = _build_section(build_priority_risk_prompt, ticket)
    sensitive_information_check = _build_section(build_sensitive_info_prompt, ticket)
    routing_recommendation = _build_section(build_routing_prompt, ticket)
    draft_customer_response = _build_section(
        build_draft_response_prompt,
        ticket,
        classification=classification,
    )
    response_quality_review = _build_section(
        build_quality_review_prompt,
        ticket,
        draft_customer_response=draft_customer_response,
    )

    config = load_config()
    final_package = {
        'ticket_summary': summary,
        'classification': classification,
        'sentiment_analysis': sentiment,
        'priority_and_risk': priority_and_risk,
        'sensitive_information_check': sensitive_information_check,
        'routing_recommendation': routing_recommendation,
        'draft_customer_response': draft_customer_response,
        'response_quality_review': response_quality_review,
        'generation_metadata': {
            'model_used': config.groq_model,
            'temperature': 0.2,
            'total_steps_completed': 8,
            'generated_at': datetime.now(timezone.utc).isoformat(),
        },
    }
    return final_package


def save_json(output: dict, path: Path) -> None:
    """Save analysis results as formatted JSON file."""
    # Ensure output directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('w', encoding='utf-8') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)


def _format_section_header(section_name: str) -> str:
    """Convert section name from snake_case to Title Case."""
    return section_name.replace("_", " ").title()


def _format_section_as_markdown(section: str, content: dict) -> list[str]:
    """Format a single analysis section with its content as markdown."""
    lines = [
        _format_section_header(section),
        '',
        '```json',
        json.dumps(content, indent=2, ensure_ascii=False),
        '```',
        '',
    ]
    return lines


def _build_markdown_output(analysis_results: dict) -> str:
    """Build complete markdown document from analysis results."""
    lines = ['# Ticket Intelligence Package', '']
    
    #### Add each analysis section
    for section, content in analysis_results.items():
        if section == 'generation_metadata':
            continue
        lines.extend(_format_section_as_markdown(section, content))
    
    #### Add metadata section at the end
    lines.extend([
        'Generation Metadata',
        '',
        '```json',
        json.dumps(analysis_results['generation_metadata'], indent=2, ensure_ascii=False),
        '```',
    ])
    
    return '\n'.join(lines)


def save_markdown(output: dict, path: Path) -> None:
    """Save analysis results as a readable markdown file."""
    # Ensure output directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    markdown_content = _build_markdown_output(output)
    with path.open('w', encoding='utf-8') as file:
        file.write(markdown_content)


def _parse_cli_arguments():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(description='AI-Powered Support Ticket Triage')
    
    parser.add_argument(
        '--input-file', '-i',
        type=Path,
        help='Path to ticket JSON input file (uses sample if not provided)'
    )
    parser.add_argument(
        '--output-file', '-o',
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help='Path to save final JSON output'
    )
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Also save a Markdown version of the output'
    )
    
    return parser.parse_args()


def _load_ticket(input_file: Path = None) -> dict:
    """Load ticket from file, or use sample ticket if no file provided."""
    if input_file:
        print(f'Loading ticket from {input_file}...')
        return load_ticket_from_file(input_file)
    
    print('Using sample ticket...')
    return SAMPLE_TICKET_INPUT  


def _save_output_files(analysis_results: dict, output_path: Path, save_markdown_version: bool) -> None:
    """Save analysis results to JSON and optionally Markdown files."""
    # Save as JSON
    save_json(analysis_results, output_path)
    print(f' JSON output saved to {output_path}')
    
    # Save as Markdown if requested
    if save_markdown_version:
        markdown_path = output_path.with_suffix('.md')
        save_markdown(analysis_results, markdown_path)
        print(f' Markdown output saved to {markdown_path}')


def main():
    """Main entry point - ticket analysis workflow."""
    # Parse command-line arguments
    args = _parse_cli_arguments()
    
    # Validate configuration
    try:
        load_config()
    except EnvironmentError as error:
        print(f'Configuration error: {error}')
        return
    
    # Load the support ticket data
    try:
        ticket = _load_ticket(args.input_file)
    except Exception as error:
        print(f' Failed to load ticket: {error}')
        return
    
    # Run the analysis pipeline
    try:
        print('Analyzing ticket')
        final_package = run_ticket_analysis(ticket)
    except Exception as error:
        print(f' Analysis failed: {error}')
        return
    
    # Save the results 
    _save_output_files(final_package, args.output_file, args.markdown)
    print('Done!')


if __name__ == '__main__':
    main()
