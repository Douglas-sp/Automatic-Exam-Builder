from django.conf import settings
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
        if self.file_extension == "docx":
            self.text = docx2txt.process(self.file_path)
        elif self.file_extension == "pptx":
            ppt = Presentation(self.file_path)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        self.text += shape.text
        elif self.file_extension == "pdf":
            pdf_reader = PdfReader(self.file_path)
            for page in pdf_reader.pages:
                self.text += page.extract_text()
        elif self.file_extension == "txt":
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

        """
        return the processed text in this format:
        Example:
        text1 = "Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace."
        text2 = "Princess Arya Stark is the third child and second daughter of Lord Eddard Stark and his wife, Lady Catelyn Stark. She is the sister of the incumbent Westerosi monarchs, Sansa, Queen in the North, and Brandon, King of the Andals and the First Men. After narrowly escaping the persecution of House Stark by House Lannister, Arya is trained as a Faceless Man at the House of Black and White in Braavos, using her abilities to avenge her family. Upon her return to Westeros, she exacts retribution for the Red Wedding by exterminating the Frey male line."
        text3 = "Dry Cleaning are an English post-punk band who formed in South London in 2018.[3] The band is composed of vocalist Florence Shaw, guitarist Tom Dowse, bassist Lewis Maynard and drummer Nick Buxton. They are noted for their use of spoken word primarily in lieu of sung vocals, as well as their unconventional lyrics. Their musical stylings have been compared to Wire, Magazine and Joy Division.[4] The band released their debut single, 'Magic of Meghan' in 2019. Shaw wrote the song after going through a break-up and moving out of her former partner's apartment the same day that Meghan Markle and Prince Harry announced they were engaged.[5] This was followed by the release of two EPs that year: Sweet Princess in August and Boundary Road Snacks and Drinks in October. The band were included as part of the NME 100 of 2020,[6] as well as DIY magazine's Class of 2020.[7] The band signed to 4AD in late 2020 and shared a new single, 'Scratchcard Lanyard'.[8] In February 2021, the band shared details of their debut studio album, New Long Leg. They also shared the single 'Strong Feelings'.[9] The album, which was produced by John Parish, was released on 2 April 2021.[10]"

        docs = [{"content": text1}, {"content": text2}, {"content": text3}]
        
        """

        docs = [{"content": text} for text in paragraphs]

        return docs

    def get_file_path(self, file):
        # use COURSE_MATERIALS_DIR from settings.py
        # to get the absolute path of the file
        return os.path.join(settings.COURSE_MATERIALS_DIR, file.split("/")[-1])

