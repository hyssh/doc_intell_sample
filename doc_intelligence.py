"""
Summary: This script reads files from a folder 'source' and analyze the document using Azure Document Intelligence.
The script saves the paragraphs and tables to a folder 'output' in markdown format.

Hyun
"""
import os
import base64
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat, AnalyzeResult 

load_dotenv()
endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")


def ai_document_analyer(file: str):
    # assert file==None, "file is required"
    assert os.path.exists(file), "file does not exist"

    document_analysis_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
        
    with open(file, "rb") as source_file:
        document_bytes = source_file.read()
    
    poller = document_analysis_client.begin_analyze_document(model_id="prebuilt-layout",
                                                             analyze_request=AnalyzeDocumentRequest(bytes_source=document_bytes),
                                                             output_content_format=ContentFormat.TEXT)
    result: AnalyzeResult = poller.result()


    # get the file name, remove file extension
    file_name = os.path.basename(file).split(".")[0]

    # if the file extension is docx, save the result.paragraphs to files 
    for paragraph_idx, paragraph in enumerate(result.paragraphs):
        with open(f"output/{file_name}_paragraph_{paragraph_idx}.txt", "w") as f:
            f.write(f"{paragraph.content}\n")

    # for page in result.pages:
    #     # save each page to a file named after file name_page number.txt
    #     if page.lines is not None:
    #         with open(f"output/{file_name}_{page.page_number}.txt", "w") as f:
    #             for line_idx, line in enumerate(page.lines):
    #                 f.write(f"{line.content}\n")    
        
    for table_idx, table in enumerate(result.tables):
        # Create a html table for table
        markdown_table = ""

        data = table.cells
        # Convert data to 2D list
        table = [["" for _ in range(max(cell.column_index for cell in data) + 1)] for _ in range(max(cell.row_index for cell in data) + 1)]  
        for cell in data:  
            table[cell.row_index][cell.column_index] = cell.content  

        # Convert 2D list to markdown  
        markdown_table = ["| " + " | ".join(row) + " |" for row in table]  
        header_seperator = ["|---" * len(table[0]) + "|"]  
        markdown_table = markdown_table[:1] + header_seperator + markdown_table[1:]  

        markdown_table = "\n".join(markdown_table)

        with open(f"output/{file_name}_table_{table_idx}.txt", "w") as f:
            # f.write(("Table # {} has {} rows and {} columns".format(table_idx, table.row_count, table.column_count)))
            f.write(f"{markdown_table}")


def main():
    # create a list has file names in a folder 'source'
    # for each file, read the file and analyze the document
    file_lists = []
    for root, dirs, files in os.walk("source"):
        for file in files:
            file_lists.append(os.path.join(root, file))

    for file in file_lists:
        print(file)
        ai_document_analyer(file)

if __name__ == "__main__":
    main()