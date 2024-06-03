# Extract table as Markdown table

This Python script uses the Azure Form Recognizer client library to analyze documents. It supports both .docx and .pdf files.

## Create Azure Resources

- Azure Cognitive Service Multi-service

> Note: Must have Azure Cognitive Service Multi-service account to process Microsoft Word (.docx) files

### Requirements

- Python 3.10 or later
- Azure Form Recognizer resource
- Python module packages
    ``` 
    python-dotenv==1.0.0
    azure-ai-documentintelligence==1.0.0b3
    ```
- .env file with ENDPOINT and KEY variables set to your Form Recognizer resource's endpoint and key

## Run code

- Download sample code from this repo
- Create Virtual Env before run the code

## Features

- Analyzes documents using Azure Form Recognizer's prebuilt layout model.
- Extracts paragraphs from .docx files and saves them as separate .txt files.
- Extracts pages from .pdf files and saves them as separate .txt files.
- Extracts tables from documents and saves them as Markdown tables in .txt files.

## Usage

- Place the documents you want to analyze in the source directory.
- Run the script with python doc_intelligence.py.
- The script will analyze each document and save the results in the output directory.

## Code Structure

- ai_document_analyer(file: str): This function takes a file path as input, reads the file, and sends it to Azure Form Recognizer for analysis. It then processes the analysis results and saves them to the output directory.
- main(): This function walks through the source directory, collects all the file paths, and sends each file to ai_document_analyer() for analysis.

## Note

This script is a sample to demonstrate the use of Azure Form Recognizer's prebuilt layout model. It may need to be modified to meet your specific needs.