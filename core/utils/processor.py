import docx2txt
from PyPDF2 import PdfReader
import textract
import os
import re
from pptx import Presentation


class DocumentProcessor:
    """
    Extracts text from a document file,
    Supports .docx, .pptx, .pdf, .txt
    """

    def __init__(self, file_path):
        self.file_path = self.get_file_path(file_path)
        self.file_extension = self.get_file_path(file_path).split(".")[-1]
        self.text = ""

    def extract_text(self):
        if self.file_extension == ".docx":
            self.text = docx2txt.process(self.file_path)
        elif self.file_extension == ".pptx":
            ppt = Presentation(self.file_path)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        self.text += shape.text
        elif self.file_extension == ".pdf":
            pdf_reader = PdfReader(self.file_path)
            for page in pdf_reader.pages:
                self.text += page.extract_text()
        elif self.file_extension == ".txt":
            with open(self.file_path, "r") as f:
                self.text = f.read()
        else:
            raise ValueError("Unsupported file extension")

    def get_text(self):
        if not self.text:
            self.extract_text()
        return self.text

    def process_text(self):
        """
        Process the text to remove unwanted characters,
        and replace them with spaces,
        and make meaningful paragraphs not just a single line
        of text.
        :return: processed string
        """
        # First, replace any unwanted characters with spaces
        self.text = re.sub('[^a-zA-Z0-9]', ' ', self.text)

        # Next, split the text into paragraphs based on common delimiters
        # such as double newlines, or combinations of newline and tab characters
        paragraphs = re.split('\n|\r\n*\r\n|\n\t*\n|\r\n\t*\r\n', self.text)

        # Finally, join the paragraphs back together with double newlines
        processed_text = '\n\n'.join(paragraphs)

        return processed_text

    def get_file_path(self, file):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file)

