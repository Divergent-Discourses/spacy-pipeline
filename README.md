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

### POS-tags
The POS tags conform to the [Universal Dependencies](https://universaldependencies.org/u/pos/) POS-tag definitions.

### NER tags
The tag set was developed specifically for the study of Tibetan language newspapers of the 1950s and 1960s. This is reflected in the POSITION and SLOGAN tags, which will less usefull in other contexts. 
- **PER (person)**: Names of individual people, including first, middle, and last names. When an honorific title or position designation appears with a personal name, the title is tagged as POSITION separately from PER.
- **ORG (organisation)**: Names of companies, government agencies, institutions, associations, and place names used as a metonym for organisations (e.g., ལྷ་ས་གྲོང་ཁྱེར་, རང་ལྗོངས་ and བོད་རང་སྐྱོང་ལྗོངས་), and other formally structured groups.
- **SOC (social groups)**: Names of unstructured social groups, including workers, ethnic groups, soldiers, academics, youth, officials.
- **TIME**: Temporal expressions including dates, times, epochs, durations, and periods.
- **LOC (location)**: Geographic locations including countries, cities, addresses, landmarks, regions, and natural features.
- **POSITION**: Religious, political, or job titles, roles, positions of authority, and honorifics. Titles (such as ཏཱ་བླ་མ་ངག་དབང་སྦྱིན་པ་ or ཤིས་ཀྲང་ཧྥུ་ཀྲུའུ་ཞི་) are categorised separately from any associated personal names, which belong in the PER category.
- **TITLE**: Names of published works, including books, articles, reports, films, songs, and other creative works or published or unpublished documents.
- **SLOGAN**: Names of policies, political ideologies, political campaigns and drives. Catchphrases, mottos, proverbs, slogans, names of theories, or memorable phrases associated with political, commercial, or cultural entities. These may appear without explicit quotation markers.
- **EVENT**: Named occasions including conferences, festivals, anniversaries, ceremonies, disasters, and historical events.

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
   git clone https://github.com/Divergent-Discourses/spacy-pipeline.git
   ``` 

* Alternatively, you can download the repository as a ZIP file.

2. Open the terminal in the directory where you cloned this repository, then set up a virtual environment and install the dependencies:
   ```bash/cmd
   python -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows (cmd)
   pip install -r requirements.txt
   pip install --no-deps thinc==8.3.6 # downgrade thinc
   ```
   
* If you encounter the error `File C:\your\directory\spacy-pipeline\venv\Scripts\Activate.ps1 cannot be loaded because
running scripts is disabled on this system` on Windows, run the following command from the root directory:
   ```cmd
   Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
   ```

* If you encounter a compilation error with the `blis` dependency, run the following command:
   ```cmd
   pip install spacy --only-binary :all:
   ```

* If you experience other installation errors that you cannot address on your own, [Anaconda/Miniconda](https://www.anaconda.com/download/success) can be used to install the necessary libraries. Nonetheless, this solution is not ideal, as it typically introduces extra, unnecessary packages that may degrade performance.

* If you encounter the following error, remove the virtual environment (`rm -r venv`) and repeat the installation starting from step 2, but skip the step that downgrades `thinc`:
   ```cmd
   Error processing text: index -1 is out of bounds for axis 0 with size 0
   ```

3. Install botok, see the [instruction](https://github.com/Divergent-Discourses/modern-botok?tab=readme-ov-file#how-to-use) in modern-botok (up to step 5 in the instructions). If modern-botok is installed on your system but not within your new virtual environment (venv), install botok there and proceed to skip all steps beyond step 2. Also modify the value of `DEFAULT_BOTOK_CONFIG_PATH` in `unified_botok_tokenizer.py` in `src` folder to point to the directory where the `pybo` folder has been created.

4. Install a Tibetan model (bo_core_news_lg). The latest model is `bo_core_news_lg-0.0.7`.
  ```bash/cmd
  pip install packages/bo_core_news_lg-0.0.7.tar.gz # Linux/macOS
  pip install packages\bo_core_news_lg-0.0.7.tar.gz # Windonws (cmd)
  ```
* If you find `bo_core_news_lg-0.0.7` to be too slow, you can instead install `bo_core_news_lg-0.0.5`, which runs significantly faster, although its performance is somewhat inferior.

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
- `--csv-file` - See [CSV Mode](#csv-mode-ner-only) below

#### CSV Mode (NER Only)

Use `--csv-file` to process a CSV file row by row. Runs **NER only**, regardless of `--task`, and output is always **JSON**, regardless of `-f/--format`. Cannot be combined with `-t/--text` or `-i/--input-file`.

**Expected CSV Columns**

| Column | Description |
|---|---|
| `normalised_paragraph` | Text used as input for NER |
| `paragraph_idx` | Output as `Id` in results |
| `filename` | Output as `Filename` in results |
| `year`, `month`, `day` | Combined into `Date` as `YYYY-MM-DD` (blanks default to `00`, blank year to `0`) |

**CSV-Specific Options**

| Option | Description |
|---|---|
| `--csv-encoding` | CSV file encoding (default: `utf-8`) |
| `--batch-size` | Number of rows processed per NER batch (default: `64`) |

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

### 6. CSV Mode (NER only)
```bash/cmd
python src/model_executor.py -m bo_core_news_lg --csv-file YOUR_CSV_FILE.csv -f json json --task ner -o results.json
```

### 7. Display Help Information

```bash/cmd
python src/model_executor.py --help
```
## Training data
will be published soon
