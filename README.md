
# Quorum Coding Challenge

This repository contains a Python solution for the Quorum Coding Challenge: working with legislative data to compute vote summaries for legislators and bills.

## Project Structure:
quorum-coding-challenge/\
├── data/ # Input CSV files\
│ ├── bills.csv\
│ ├── legislators.csv\
│ ├── votes.csv\
│ └── vote_results.csv\
├── output/ # Generated CSV files (ignored by Git)\
├── src/ # Python source code\
│ └── quorum_analysis_output.py\
├── README.md\
└── .gitignore

## Getting Started

### 1. Clone the repository:

```bash
git clone https://github.com/marcus-nl-2018/quorum-coding-challenge.git
cd quorum-coding-challenge
```

### 2. Install dependencies:
This project uses Python 3 and pandas:
```bash
pip install pandas
```

This project uses Python 3 and pandas:
```bash
pip install tqdm
```

### 3. Place your input CSVs in the data/ folder
* legislators.csv
* bills.csv
* votes.csv
* vote_results.csv

The script automatically detects CSV filenames based on keywords.

### 4. Run the script:
Default usage (outputs saved to output/):
```bash
python src/quorum_analysis_output.py --output_folder ./output
```

### 5.Check the output/ folder for the following files:
* legislators-support-oppose-count.csv
* bills-support-oppose-count.csv


## Features
* Automatically detects input CSV files in data/.
* Vectorized for fast performance on large datasets.
* Prints top legislators and bills for verification.
* Optional output folder for generated CSVs.

## Notes
* If any primary sponsor is missing in the legislators data, the script will label it as "Unknown".
* The script can be easily extended for additional metrics or new columns.

## License
This project is created for the <b>Quorum Coding Challenge




