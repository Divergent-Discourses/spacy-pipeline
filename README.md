# Tibetan spaCy NLP Processor

## Overview

This tool processes Modern Tibetan text using spaCy models to perform Named Entity Recognition (NER) and Part-of-Speech (POS) tagging. It's specifically designed for Tibetan language processing with specialized tokenizers that handle Tibetan script characteristics.

## Features

- **Named Entity Recognition (NER)**: Identifies and classifies entities in Tibetan text
- **Part-of-Speech Tagging**: Tags grammatical roles of tokens
- **Flexible Processing**: Run NER only, POS only, or both together
- **Multiple Output Formats**: JSON, human-readable text, or CSV
- **File and Text Input**: Process text directly or from files
- **Tibetan-Specific Tokenization**: Uses specialized tokenizers for accurate Tibetan text processing

## Requirements

- Python 3.6+
- spaCy
- Tibetan spaCy model (e.g., `bo_core_news_lg`)
- Custom dependencies:
  - `botok_loader.BoTokTokenizer`
  - `unified_botok_tokenizer`

## Installation

1. Install spaCy and your Tibetan model:
   ```bash
   pip install spacy
   # Install your specific Tibetan model
   ```

2. Ensure the custom tokenizer modules are available in your Python path.

## Usage

### Basic Command Structure

```bash
python model_executor.py -m <model_name> [options] <input>
```

### Required Arguments

- **Model**: `-m, --model` - SpaCy model name/path for both NER and POS tagging
- **Input**: Either `-t, --text` for direct text input OR `-i, --input-file` for file input

### Optional Arguments

- `--task {ner,pos,full}` - Task to perform (default: full)
- `-f, --format {json,text,csv}` - Output format (default: text)
- `-o, --output` - Output file path (prints to stdout if not specified)

## Examples

### 1. Basic Text Processing (Full Analysis)

```bash
python model_executor.py -m bo_core_news_lg -t "དེ་རིང་ང་ལགས་པའི་འདུ་འཁྲིལ་ལ་འགྲོ་དགོས།"
```

### 2. Named Entity Recognition Only

```bash
python model_executor.py -m bo_core_news_lg -t "བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ་ཤི་ག་རྩེ་རྫོང་ཁུལ་དུ་ཡོད།" --task ner
```

### 3. Part-of-Speech Tagging Only

```bash
python model_executor.py -m bo_core_news_lg -t "ང་ལ་དཔེ་ཆ་དགོས།" --task pos
```

### 4. Process File with JSON Output

```bash
python model_executor.py -m bo_core_news_lg -i input.txt -f json -o results.json
```

### 5. CSV Output for Further Analysis

```bash
python model_executor.py -m bo_core_news_lg -i document.txt -f csv -o analysis.csv
```

## Output Formats

### Text Format (Default)
Human-readable format with clear sections for entities and tokens:

```
==================================================
NLP ANALYSIS RESULTS
==================================================
Input Text: [your text]
Total Entities: 2
Total Tokens: 8

NAMED ENTITIES:
--------------------
1. བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ
   Label: ORG (Organizations, companies, agencies, institutions, etc.)
   Position: 0-20

TOKENS (POS TAGGING):
-------------------------
'བཀྲ་ཤིས་' - POS: NOUN
'ལྷུན་པོ་' - POS: NOUN
...
```

### JSON Format
Structured data format suitable for programmatic processing:

```json
{
  "input_text": "བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ་ཤི་ག་རྩེ་རྫོང་ཁུལ་དུ་ཡོད།",
  "entities": [
    {
      "text": "བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ",
      "label": "ORG",
      "start": 0,
      "end": 20,
      "description": "Organizations, companies, agencies, institutions, etc."
    }
  ],
  "tokens": [
    {
      "text": "བཀྲ་ཤིས་",
      "pos": "NOUN",
      "is_alpha": true,
      "is_stop": false,
      "is_punct": false,
      "dep": "compound",
      "head": "ལྷུན་པོ་"
    }
  ],
  "entity_count": 1,
  "token_count": 8
}
```

### CSV Format
Tabular format for spreadsheet analysis:

```csv
Type,Text,Label,Description,Start,End
Entity,"བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ",ORG,"Organizations, companies, agencies, institutions, etc.",0,20

Type,Text,POS,IsAlpha,IsStop,IsPunct,Dependency,Head
Token,"བཀྲ་ཤིས་",NOUN,True,False,False,compound,"ལྷུན་པོ་"
Token,"ལྷུན་པོ་",NOUN,True,False,False,nsubj,"ཡོད"
```