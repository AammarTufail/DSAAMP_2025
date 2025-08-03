# DJANGO

## Installation

### miniconda
```bash
conda create -n django python=3.11 -y
conda activate django
pip install django
```

### python env
```bash
python -m venv .venv
source .venv/bin/activate # for Linux/Mac
.venv\Scripts\activate # for Windows
pip install django
```

## Create a Django project
```bash
django-admin startproject codanics # codanics is the project name
cd codanics
python manage.py runserver
```