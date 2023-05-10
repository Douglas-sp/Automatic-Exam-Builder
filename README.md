# Automatic Exam Builder

The automatic exam builder is the system that will help users save time and ease the process of setting exams since the exams will be automatically generated other than being set manually which is time-consuming and hectic

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to install the following software:

* [Elasticsearch](https://www.elastic.co/downloads/elasticsearch)
* [Python](https://www.python.org/downloads/)
* [JDK](https://www.oracle.com/java/technologies/javase-downloads.html)

### Installing

```bash
git clone <repo-url>
cd <repo-name>
pip install -r requirements.txt
```

### Running

```bash
# Start Elasticsearch first
./elasticsearch-<version.number>/bin/elasticsearch.bat # Windows
./elasticsearch-<version.number>/bin/elasticsearch # Linux

# Start the server
python manage.py runserver
```
