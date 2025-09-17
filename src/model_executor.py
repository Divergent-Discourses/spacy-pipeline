#!/usr/bin/env python3
import argparse
import json
import sys
import spacy
from typing import Dict, Optional
from botok_loader import BoTokTokenizer
from unified_botok_tokenizer import create_spacy_tokenizer_factory


class SpacyNLPProcessor:
    def __init__(self, model_name: str = None):
        """
        Initialize the unified NLP processor with separate models and tokenizers for NER and POS tagging.

        Args:
            model_name: SpaCy model name/path both for NER and POS-tagging
        """
        self.nlp = spacy.load(model_name)

    def perform_ner(self, text: str) -> Dict:
        """Perform Named Entity Recognition on the input text."""
        self.nlp.tokenizer = create_spacy_tokenizer_factory(
            force_split_tsheg=True
        )(self.nlp)

        doc = self.nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })

        return {
            "input_text": text,
            "entities": entities,
            "entity_count": len(entities)
        }

    def perform_pos_tagging(self, text: str) -> Dict:
        """Perform Part-of-Speech tagging on the input text."""
        self.nlp.tokenizer = BoTokTokenizer(self.nlp)

        doc = self.nlp(text)

        tokens = []
        for token in doc:
            tokens.append({
                "text": token.text,
                "pos": token.pos_,
                "is_alpha": token.is_alpha,
                "is_stop": token.is_stop,
                "is_punct": token.is_punct
            })

        return {
            "input_text": text,
            "tokens": tokens,
            "token_count": len(tokens),
        }

    def process_text_full(self, text: str) -> Dict:
        """Process text with both NER and POS tagging."""
        ner_results = self.perform_ner(text)
        pos_results = self.perform_pos_tagging(text)

        return {
            "input_text": text,
            "entities": ner_results["entities"],
            "tokens": pos_results["tokens"],
            "entity_count": ner_results["entity_count"],
            "token_count": pos_results["token_count"]
        }

    def export_results(self, results: Dict, output_format: str, output_file: Optional[str] = None):
        """Export the results in the specified format."""
        if output_format.lower() == 'json':
            output = json.dumps(results, ensure_ascii=False, indent=2)
        elif output_format.lower() == 'text':
            output = self.format_as_text(results)
        elif output_format.lower() == 'csv':
            output = self.format_as_csv(results)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results exported to: {output_file}")
        else:
            print(output)

    def format_as_text(self, results: Dict) -> str:
        """Format results as human-readable text."""
        output = []
        output.append("=" * 50)
        output.append("NLP ANALYSIS RESULTS")
        output.append("=" * 50)
        output.append(f"Input Text: {results['input_text']}")

        if 'entity_count' in results:
            output.append(f"Total Entities: {results['entity_count']}")
        if 'token_count' in results:
            output.append(f"Total Tokens: {results['token_count']}")

        output.append("")

        # Display entities if present
        if 'entities' in results and results['entities']:
            output.append("NAMED ENTITIES:")
            output.append("-" * 20)
            for i, entity in enumerate(results['entities'], 1):
                output.append(f"{i}. {entity['text']}")
                # output.append(f"   Label: {entity['label']} ({entity['description']})")
                output.append(f"   Label: {entity['label']}")
                output.append(f"   Position: {entity['start']}-{entity['end']}")
                output.append("")
        elif 'entities' in results:
            output.append("No named entities found.")
            output.append("")

        # Display tokens if present
        if 'tokens' in results and results['tokens']:
            output.append("TOKENS (POS TAGGING):")
            output.append("-" * 25)
            for token in results['tokens']:
                output.append(f"'{token['text']}' - POS: {token['pos']}")

        return "\n".join(output)

    def format_as_csv(self, results: Dict) -> str:
        """Format results as CSV."""
        output = []

        # If entities are present, format as entity CSV
        if 'entities' in results and results['entities']:
            output.append("Type,Text,Label,Start,End")
            for entity in results['entities']:
                output.append(
                    f'Entity,"{entity["text"]}",{entity["label"]},{entity["start"]},{entity["end"]}')

        # If tokens are present, add token information
        if 'tokens' in results and results['tokens']:
            if output:  # Add separator if entities were already added
                output.append("")
            output.append("Type,Text,POS,IsAlpha,IsStop,IsPunct")
            for token in results['tokens']:
                output.append(
                    f'Token,"{token["text"]}",{token["pos"]},{token["is_alpha"]},{token["is_stop"]},{token["is_punct"]}')

        return "\n".join(output)


def create_argument_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Process text using spaCy models for NER and POS tagging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python model_executor.py -m bo_core_news_lg -t "Your text here"
        """
    )

    # Model arguments
    model_group = parser.add_argument_group('Model Configuration')
    model_group.add_argument('-m', '--model',
                             help='SpaCy model for both NER and POS (if using same model)')

    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', '--text',
                             help='Input text to process')
    input_group.add_argument('-i', '--input-file',
                             help='Path to input text file')

    # Processing options
    parser.add_argument('--task', choices=['ner', 'pos', 'full'],
                        default='full', help='Task to perform (default: full)')
    parser.add_argument('-f', '--format', choices=['json', 'text', 'csv'],
                        default='text', help='Output format (default: text)')
    parser.add_argument('-o', '--output',
                        help='Output file path (if not specified, prints to stdout)')

    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    # Determine models to use
    if not args.model:
            print("Error: Must specify either --model or at least one of --ner-model/--pos-model")
            sys.exit(1)

    # Initialize processor
    processor = SpacyNLPProcessor(model_name=args.model)

    # Get input text
    if args.text:
        input_text = args.text
    else:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            input_text = f.read().strip()

    # Process text based on task
    try:
        if args.task == 'ner':
            results = processor.perform_ner(input_text)
        elif args.task == 'pos':
            results = processor.perform_pos_tagging(input_text)
        else:  # full processing
            results = processor.process_text_full(input_text)

        processor.export_results(results, args.format, args.output)
    except Exception as e:
        print(f"Error processing text: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()