### Steps to Run Project

### using docker
``
docker build -t pdf-parser .
docker run -p 5001:5000 \
  -e UPLOAD_FOLDER=<your-prefered-path> \
  -e TASK_FOLDER=<your-prefered-path> \
  -e ALLOWED_EXTENSIONS=pdf \
  -v $(pwd):/app \
  pdf-parser
``

### using python
1. make sure you have .env file
2. run
``
python main.py
``


## File and Folder Structure
```commandline
├── main.py
├── processor
│   ├── __init__.py
│   └── file_processor.py
├── requirements.txt
└── utils
    ├── __init__.py
    ├── parser
    │   ├── __init__.py
    │   ├── parser.py
    │   └── pdf_parser.py
    └── writer
        ├── __init__.py
        ├── csv_writer.py
        └── writer.py
```


### utils
utils section is a utility module for the project.
Utility can parse and write files.

### processor
processor section is a processor module for the project.
Processor can process the files.

### main
main section is a main module for the project.
Main module is used to run the project.