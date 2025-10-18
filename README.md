# Statica

A domain-specific programming language designed for statistical analysis and reporting.

## Overview

Statica provides a clean, English-like syntax for performing statistical tests, regression modeling, and data visualization with automatic human-readable conclusions. The language interprets user-written `.sta` scripts through a custom parser and execution engine built in Python, making statistical analysis approachable, transparent, and expressive.

## Key Features

- **Natural Language Syntax**: Simple, intuitive commands that read like English
- **Comprehensive Statistical Tests**: Built-in support for one-sample t-tests, linear regression modeling, and scatter plot generation
- **Automatic Interpretation**: Human-readable conclusions generated automatically from statistical results
- **Interactive Analysis**: Context-aware system that prompts for missing statistical table values when needed
- **Extensible Architecture**: Modular design allows easy addition of new commands and statistical tests

## Quick Start Example

```statica
data = load "study.csv"

t = test ttest mean of data.score = 75

m = regress score ~ age + group on data

plot data.age vs data.score scatter

conclude t
conclude m
```

**Expected Output:**

```
[Loaded study.csv]
[Ran t-test on score]
[Ran regression: score ~ age + group]
[Plot displayed: age vs score]

The mean (72.34) is significantly different from 75 (t = -2.14, p = 0.037).

Model Summary:
==========================
Dep. Variable: score
R-squared: 0.742
P > |t|: 0.001
==========================
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/HirulaAbesignha/statica-proto.git
cd statica
```

2. **Create Virtual Environment** (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

**Required Dependencies:**

- lark-parser
- pandas
- matplotlib
- scipy
- statsmodels

## Project Structure

```
statica-proto/
├── README.md
├── requirements.txt
├── examples/
│   ├── study.csv
│   └── example.sta
└── statica/
    ├── __init__.py
    ├── grammar.lark
    ├── parser.py
    ├── runtime.py
    ├── nlg.py
    └── cli.py

```

## Usage

### Running a Statica Program

**From source:**

```bash
python -m src.cli examples/program.sta
```

**After installation:**

```bash
statica examples/program.sta
```

### Command Reference

#### Data Loading
```statica
data = load "filename.csv"
```

#### Statistical Tests
```statica
t = test ttest mean of data.column = value
```

#### Regression Analysis
```statica
m = regress dependent ~ independent1 + independent2 on data
```

#### Visualization
```statica
plot data.x vs data.y scatter
```

#### Generate Conclusions
```statica
conclude t
conclude m
```

## Architecture

### 1. Lexing and Parsing

Statica uses the Lark parser to define its grammar and interpret `.sta` code. The parser reads source code and converts it into an Abstract Syntax Tree (AST) for execution.

### 2. Execution Engine

The `StaticaExec` engine walks through the AST and executes each instruction sequentially:

- Loads CSV data into Pandas DataFrames
- Performs statistical tests using SciPy and StatsModels
- Generates visualizations using Matplotlib
- Produces human-readable conclusions

### 3. Automatic Interpretation

The `conclude` command analyzes test or model results and generates natural language interpretations:

**Significant Result:**
```
The mean (72.34) is significantly different from 75 (t = -2.14, p = 0.037).
```

**Non-Significant Result:**
```
No significant difference between the sample mean (74.56) and 75 (t = -1.02, p = 0.32).
```

## Extending Statica

Statica's modular architecture supports easy extension:

### Adding New Commands

1. **Update Grammar**: Modify `grammar.lark` to define new syntax rules
2. **Implement Logic**: Add corresponding Python logic in `interpreter.py`
3. **Test**: Create test cases for the new functionality

### Suggested Extensions

- **ANOVA**: One-way and multi-way analysis of variance
- **Chi-Square Tests**: Categorical data analysis
- **Correlation Analysis**: Pearson and Spearman correlation
- **Additional Plots**: Boxplots, histograms, heatmaps
- **Data Preprocessing**: Filtering, transformation, aggregation

## Development Roadmap

### Planned Features

- **Enhanced Statistical Library**: ANOVA, chi-square, correlation tests
- **Interactive Mode**: REPL for exploratory analysis
- **Report Generation**: Export results to PDF or Markdown
- **Advanced Error Handling**: Detailed diagnostics and suggestions
- **Data Validation**: Automatic checking for statistical assumptions
- **Multiple Dataset Support**: Work with multiple data sources simultaneously

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes with clear messages
4. Submit a pull request with a detailed description

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute Statica for personal or commercial projects.

## Author

**Hirula**  
AI Engineering Student, SLIIT

## Acknowledgments

Built with:
- [Lark Parser](https://github.com/lark-parser/lark) - Parsing framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [SciPy](https://scipy.org/) - Scientific computing
- [StatsModels](https://www.statsmodels.org/) - Statistical modeling
- [Matplotlib](https://matplotlib.org/) - Data visualization

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.