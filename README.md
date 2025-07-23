#  Project: Generative AI for Irish Real Estate Data Analysis
- This project combines real-world housing data analysis with the power of Generative AI using OpenAI’s language models. The goal was to extract insights from Irish housing market listings, summarize them automatically, and ensure reliability with automated testing and CI/CD workflows.

## Problem Statement
- Real estate data is often messy, inconsistent, and difficult to interpret at scale. Market summaries typically require manual analysis. This project explores how generative AI can automate market analysis and generate high-level insights from raw data, enabling realtors or analysts to quickly understand trends.


## Project Overview

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Data Source                | CSV export of Irish housing listings from Kaggle                           |
| Language Model             | GPT-3.5 Turbo via OpenAI API                                                |
| Functionality              | Clean housing data, compute statistics, generate summaries via GPT          |
| Testing                    | Pytest unit tests for key data-cleaning functions                           |
| CI/CD                      | GitHub Actions pipeline to run tests on each push                           |
| Optional EDA               | Exploratory Data Analysis using correlation matrices and data inspection    |

---

## Project Steps

### 1. **Setup and Environment**
- Created a virtual environment using `venv`
- Installed dependencies: `pandas`, `openai`, `python-dotenv`, `pytest`
- Added `.env` file to store the `OPENAI_API_KEY`
- Created a `.gitignore` to exclude `.venv`, `__pycache__`, and `.env`

### 2. **Data Cleaning Functions**
- `clean_price(value)`: Cleans price strings like `€350,000` or `AMV: 1,200,000`
- `extract_number(value)`: Extracts numeric values from strings like `3 Bed`, `2.5 Bath`

### 3. **Main Analysis Script (`analysis.py`)**
- Loads and cleans housing data
- Computes average prices, bedrooms, bathrooms, and more
- Forms a prompt from the statistics
- Sends it to OpenAI GPT to generate a natural language summary
- Saves the generated text to `housing_summary.txt`

### 4. **Exploratory Data Analysis (EDA)**
- Added in-script EDA:  
  - `df.head()`, `df.info()`, `df.isna().sum()`
  - Generated correlation matrix
  - Dropped low-correlation columns before analysis

### 5. **Unit Testing**
- Created `tests/test_analysis.py`
- Wrote tests for:
  - `extract_number()`
  - `clean_price()`
- Verified edge cases and robustness

### 6. **CI/CD Integration**
- Set up GitHub Actions:
  - Installs Python + dependencies
  - Runs `pytest`
  - Fails the build if any tests break
- Includes `--junitxml=report.xml` for test reporting

### 7. **GitHub Project Structuring**

- `Gen-AI-Irish-Real-Estate-Markey-Data-Analysis/`
  - `.github/workflows/main.yml` – GitHub Actions workflow
  - `data/daft_housing_data.csv` – Raw CSV data
  - `analysis.py` – Main script with GPT integration
  - `eda.py` – EDA script (optional)
  - `tests/`
    - `test_analysis.py` – Unit tests
  - `requirements.txt` – Project dependencies
  - `.gitignore` – Excludes venv, .env, etc.
  - `README.md` – Project overview
  - `housing_summary.txt` – AI-generated output

### Tools & Technologies Used
- **Python 3.11** --> Programming language
- **Pandas** --> Data cleaning & aggregation
- **OpenAI SDK** --> AI-generated text summaries
- **pytest** --> Unit testing framework
- **GitHub Actions**  --> Continuous Integration pipeline
- **.env + dotenv** -->	Secure API key handling
- **Git / GitHub**	--> Version control and collaboration
- **Visual Studio Code**  --> IDE




