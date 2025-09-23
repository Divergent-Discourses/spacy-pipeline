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

1. Open the terminal (macOS/Linux) or Command Prompt (Windows), and clone this repository:
   ```bash/cmd
   git clone git@github.com:Divergent-Discourses/spacy-pipeline.git
   ``` 

* Alternatively, you can download the repository as a ZIP file.

2. Open the terminal in the directory where you cloned this repository, then set up a virtual environment and install the dependencies:
   ```bash/cmd
   python -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows (cmd)
   pip install -r requirements.txt
   ```
   
* If you encounter the error `File C:\your\directory\spacy-pipeline\venv\Scripts\Activate.ps1 cannot be loaded because
running scripts is disabled on this system` on Windows, run the following command from the root directory:
   ```cmd
   Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
   ```

3. Install botok, see the [instruction](https://github.com/Divergent-Discourses/modern-botok?tab=readme-ov-file#how-to-use) in modern-botok (up to step 5 in the instructions). Also modify the value of `DEFAULT_BOTOK_CONFIG_PATH` in `unified_botok_tokenizer.py` in `src` folder to point to the directory where the `pybo` folder has been created.

4. Install a Tibetan model (bo_core_news_lg). The latest model is `bo_core_news_lg-0.0.7`.
  ```bash/cmd
  pip install packages/bo_core_news_lg-0.0.7/dist/bo_core_news_lg-0.0.7.tar.gz # Linux/macOS
  pip install packages\bo_core_news_lg-0.0.7\dist\bo_core_news_lg-0.0.7.tar.gz # Windonws (cmd)
  ```

## Evaluation
   Coming soon.

## Usage

### Basic Command Structure
Run the commands in the root directory where you cloned this repository.

```bash/cmd
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

You can run the following example commands from the root directory where you cloned this repository.

### 1. Basic Text Processing (Full Analysis)

```bash/cmd
python src/model_executor.py -m bo_core_news_lg -t "དེ་རིང་ང་ལགས་པའི་འདུ་འཁྲིལ་ལ་འགྲོ་དགོས།"
```

### 2. Named Entity Recognition Only

```bash/cmd
python src/model_executor.py -m bo_core_news_lg -t "བཀྲ་ཤིས་ལྷུན་པོ་དགོན་པ་ཤི་ག་རྩེ་རྫོང་ཁུལ་དུ་ཡོད།" --task ner
```

### 3. Part-of-Speech Tagging Only

```bash/cmd
python src/model_executor.py -m bo_core_news_lg -t "ང་ལ་དཔེ་ཆ་དགོས།" --task pos
```

### 4. Process File with JSON Output

```bash/cmd
python src/model_executor.py -m bo_core_news_lg -i input.txt -f json -o results.json
```

### 5. CSV Output for Further Analysis

```bash/cmd
python src/model_executor.py -m bo_core_news_lg -i document.txt -f csv -o analysis.csv
```

### 6. Display Help Information

```bash/cmd
python src/model_executor.py --help
```