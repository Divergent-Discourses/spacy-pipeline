#!/usr/bin/env python3
"""
model_executor-csv-text.py

This script extends the original model executor while preserving its original behavior for:
  - single text input (-t / --text)
  - text file input (-i / --input-file)
  - task flags (--task ner | pos | full)
  - output flags (-f / --format, -o / --output)

The only added functionality is CSV-based NER:
  - use --csv-file to process a CSV row by row
  - in CSV mode, the script runs NER only
  - JSON output contains one entry per CSV row, with metadata plus extracted entities

CSV mode for the current format expects:
  - normalised_paragraph  -> text used for NER
  - paragraph_idx         -> output as Id
  - filename              -> output as Filename
  - year, month, date     -> combined into Date as YYYY-MM-DD
    (blank month/day become 00; blank year becomes 0000)

Change made in this version:
  - input_text is ALWAYS included in the JSON output for CSV NER mode
"""

import argparse
import csv
import json
import sys
from typing import Dict, Optional, List, Any

import spacy

from botok_loader import BoTokTokenizer
from unified_botok_tokenizer import create_spacy_tokenizer_factory


class SpacyNLPProcessor:
    def __init__(self, model_name: str):
        """
        model_name: spaCy model name (installed package) or path to model data dir.
        """
        self.nlp = spacy.load(model_name)

    # ----------------------------
    # NER (unified tokenizer)
    # ----------------------------
    def _configure_ner_tokenizer(self) -> None:
        self.nlp.tokenizer = create_spacy_tokenizer_factory(force_split_tsheg=True)(self.nlp)

    def perform_ner(self, text: str) -> Dict[str, Any]:
        """Run NER on a single text and return entities."""
        self._configure_ner_tokenizer()
        with self.nlp.select_pipes(enable=["ner"]):
            doc = self.nlp(text)

        entities = [
            {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
            for ent in doc.ents
        ]
        return {
            "input_text": text,
            "entities": entities,
            "entity_count": len(entities),
        }

    # ----------------------------
    # CSV NER mode
    # ----------------------------
    # This function is the only addition relative to the original script.
    # It reads a CSV file row by row, takes the text from the configured content column,
    # runs NER only, and returns JSON-style row results with metadata + entities.
    def perform_ner_on_csv(
        self,
        csv_path: str,
        content_col: str = "normalised_paragraph",
        id_col: str = "paragraph_idx",
        filename_col: str = "filename",
        year_col: str = "year",
        month_col: str = "month",
        day_col: str = "date",
        encoding: str = "utf-8",
        batch_size: int = 64,
    ) -> List[Dict[str, Any]]:
        """
        Read a CSV and run NER on the configured text column.

        Expected CSV columns for the current format:
          - normalised_paragraph  -> text used for NER
          - paragraph_idx         -> output as Id
          - filename              -> output as Filename
          - year, month, date     -> combined into Date as YYYY-MM-DD

        Returns a list of per-row results. One JSON object is produced for each CSV row,
        even when no entities are found.

        This version always includes:
          - input_text
        in the JSON output.
        """
        rows: List[Dict[str, str]] = []
        texts: List[str] = []

        with open(csv_path, "r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError("CSV appears to have no header row.")

            # case-insensitive matching of expected columns
            fn_map = {name.lower(): name for name in reader.fieldnames}

            def resolve(col: str) -> str:
                key = col.lower()
                if key not in fn_map:
                    raise ValueError(
                        f"Missing required column '{col}'. Found columns: {reader.fieldnames}"
                    )
                return fn_map[key]

            id_col_r = resolve(id_col)
            content_col_r = resolve(content_col)
            filename_col_r = resolve(filename_col)
            year_col_r = resolve(year_col)
            month_col_r = resolve(month_col)
            day_col_r = resolve(day_col)

            for row in reader:
                text = (row.get(content_col_r) or "").strip()

                year_val = str(row.get(year_col_r, "")).strip() or "0000"
                month_val = str(row.get(month_col_r, "")).strip() or "00"
                day_val = str(row.get(day_col_r, "")).strip() or "00"

                date_val = f"{year_val.zfill(4)}-{month_val.zfill(2)}-{day_val.zfill(2)}"

                rows.append(
                    {
                        "Id": row.get(id_col_r),
                        "Filename": row.get(filename_col_r),
                        "Date": date_val,
                    }
                )
                texts.append(text)

        # Configure unified tokenizer once for CSV NER
        self._configure_ner_tokenizer()

        results: List[Dict[str, Any]] = []
        with self.nlp.select_pipes(enable=["ner"]):
            for meta, doc in zip(rows, self.nlp.pipe(texts, batch_size=batch_size)):
                ents = [
                    {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
                    for ent in doc.ents
                ]
                out = {
                    "Id": meta.get("Id"),
                    "Filename": meta.get("Filename"),
                    "Date": meta.get("Date"),
                    "input_text": doc.text,   # ALWAYS INCLUDED
                    "entity_count": len(ents),
                    "entities": ents,
                }
                results.append(out)

        return results

    # ----------------------------
    # POS (botok_loader tokenizer)
    # ----------------------------
    def perform_pos_tagging(self, text: str) -> Dict[str, Any]:
        """Perform Part-of-Speech tagging on the input text."""
        self.nlp.tokenizer = BoTokTokenizer(self.nlp)
        doc = self.nlp(text)

        tokens = [
            {
                "text": token.text,
                "pos": token.pos_,
                "is_alpha": token.is_alpha,
                "is_stop": token.is_stop,
                "is_punct": token.is_punct,
            }
            for token in doc
        ]
        return {"input_text": text, "tokens": tokens, "token_count": len(tokens)}

    def process_text_full(self, text: str) -> Dict[str, Any]:
        """Process text with both NER and POS tagging."""
        ner_results = self.perform_ner(text)
        pos_results = self.perform_pos_tagging(text)
        return {
            "input_text": text,
            "entities": ner_results["entities"],
            "tokens": pos_results["tokens"],
            "entity_count": ner_results["entity_count"],
            "token_count": pos_results["token_count"],
        }

    # ----------------------------
    # Output formatting
    # ----------------------------
    def export_results(self, results: Any, output_format: str, output_file: Optional[str] = None) -> None:
        if output_format.lower() == "json":
            output = json.dumps(results, ensure_ascii=False, indent=2)
        else:
            raise ValueError("For CSV-input NER, use JSON output (-f json).")

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Results exported to: {output_file}")
        else:
            print(output)


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="Process Tibetan text using spaCy (NER/POS) and custom tokenizers"
    )

    parser.add_argument("-m", "--model", required=True, help="spaCy model name/path")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-t", "--text", help="Input text to process")
    input_group.add_argument("-i", "--input-file", help="Path to input text file")
    input_group.add_argument(
        "--csv-file",
        help="Path to input CSV file for row-by-row NER extraction",
    )

    parser.add_argument("--task", choices=["ner", "pos", "full"], default="full")
    parser.add_argument("-f", "--format", choices=["json", "text", "csv"], default="text")
    parser.add_argument("-o", "--output", help="Output file path (optional)")

    # CSV-specific options
    parser.add_argument("--csv-encoding", default="utf-8", help="CSV encoding (default: utf-8)")
    parser.add_argument("--batch-size", type=int, default=64, help="NER batching for CSV mode (default: 64)")

    return parser


def main():
    args = create_argument_parser().parse_args()

    processor = SpacyNLPProcessor(model_name=args.model)

    try:
        # CSV mode: supports NER only, outputs JSON
        if args.csv_file:
            if args.task != "ner":
                raise ValueError("CSV mode currently supports only --task ner.")
            if args.format.lower() != "json":
                raise ValueError("CSV mode outputs JSON only. Use -f json.")

            results = processor.perform_ner_on_csv(
                csv_path=args.csv_file,
                encoding=args.csv_encoding,
                batch_size=args.batch_size,
            )
            processor.export_results(results, "json", args.output)
            return

        # Text / file mode (original behavior)
        if args.text:
            input_text = args.text
        else:
            with open(args.input_file, "r", encoding="utf-8") as f:
                input_text = f.read().strip()

        if args.task == "ner":
            results = processor.perform_ner(input_text)
            if args.format.lower() != "json":
                args.format = "json"
        elif args.task == "pos":
            results = processor.perform_pos_tagging(input_text)
            if args.format.lower() != "json":
                args.format = "json"
        else:
            results = processor.process_text_full(input_text)
            if args.format.lower() != "json":
                args.format = "json"

        processor.export_results(results, args.format, args.output)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()