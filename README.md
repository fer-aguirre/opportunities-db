# Opportunities Database
Scraper to extract data from opportunity-related websites (e.g. funds, scholarships, etc.) and convert them into structured data.

## Directory Structure
```
├── .github
│   └── workflows
│       └── update-data.yml
├── .gitignore
├── LICENSE
├── Makefile
├── Pipfile
├── Pipfile.lock
├── README.md
├── assets
│   └── new_version.csv
├── data
│   ├── processed
│   │   ├── opportunities.db
│   │   └── opportunities_db.csv
│   └── raw
│       └── opportunities_urls.csv
├── docs
│   ├── data-dictionary.md
│   ├── explore-data.md
│   ├── references
│   └── reports
│       ├── index.html
│       └── style.css
├── log.txt
├── notebooks
│   ├── 0.0-analyzing-data.ipynb
│   └── 0.1-create-database.ipynb
├── opportunities_db
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── analyze.py
│   │   ├── export.py
│   │   ├── load.py
│   │   └── process.py
│   └── utils
│       ├── __init__.py
│       └── paths.py
├── outputs
│   ├── figures
│   └── tables
├── package.json
├── process-data.py
├── requirements.txt
├── setup.py
└── yarn.lock
```
---

## License

This project is released under [MIT License](/LICENSE).

---

This repository was generated with [cookiecutter](https://github.com/cookiecutter/cookiecutter).