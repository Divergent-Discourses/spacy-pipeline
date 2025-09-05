# Tibetan spaCy NLP Processor

## Overview

The spaCy pipeline `bo_core_news_lg` includes both a Part-of-Speech (POS) tagger and a Named Entity Recognizer (NER), designed for Tibetan language processing. The POS tagger and the NER rely on different Tibetan tokenizers: the POS tagger calls `botok` via `botok_loader.py`, whereas the NER component employs a customized version of `botok` (`unified_botok_tokenizer.py`).


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

1. Install botok, see the [instruction](https://github.com/Divergent-Discourses/modern-botok?tab=readme-ov-file#how-to-use) in modern-botok. Also modify the value of `DEFAULT_BOTOK_CONFIG_PATH` in `unified_botok_tokenizer.py` to point to the directory where the `pybo` folder has been created.

2. Install a Tibetan model (bo_core_news_lg).
      ```bash
      pip install packages/bo_core_news_lg-0.0.5/dist/bo_core_news_lg-0.0.5.tar.gz # Linux/macOS
      pip install packages\bo_core_news_lg-0.0.5\dist\bo_core_news_lg-0.0.5.tar.gz # Windonws (cmd)
      ```

3. Set up a virtual environment and install dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows (cmd)
   pip install -r requirements.txt
   ```
   
## Usage

### Basic Command Structure
Run the commands in the root directory where the `src` folder is located.

```bash
python src/model_executor.py -m <model_name> [options] <input>
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
python src/model_executor.py -m bo_core_news_lg -t "དེ་རིང་ང་ལགས་པའི་འདུ་འཁྲིལ་ལ་འགྲོ་དགོས།"
```

### 2. Named Entity Recognition Only

```bash
python src/model_executor.py -m bo_core_news_lg -t "བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ་ཤི་ག་རྩེ་རྫོང་ཁུལ་དུ་ཡོད།" --task ner
```

### 3. Part-of-Speech Tagging Only

```bash
python src/model_executor.py -m bo_core_news_lg -t "ང་ལ་དཔེ་ཆ་དགོས།" --task pos
```

### 4. Process File with JSON Output

```bash
python src/model_executor.py -m bo_core_news_lg -i input.txt -f json -o results.json
```

### 5. CSV Output for Further Analysis

```bash
python src/model_executor.py -m bo_core_news_lg -i document.txt -f csv -o analysis.csv
```

### 6. Display Help Information

```bash
python src/model_executor.py --help
```