from pprint import pprint
from tqdm.auto import tqdm
from haystack.nodes import QuestionGenerator, BM25Retriever, FARMReader
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.pipelines import (
    QuestionGenerationPipeline,
    RetrieverQuestionGenerationPipeline,
    QuestionAnswerGenerationPipeline,
)
from haystack.utils import launch_es, print_questions


class ExamGenerator:
    """
    A class that generates questions and answers for a set of documents.

    Attributes:
        document_store (ElasticsearchDocumentStore): An Elasticsearch document store for storing and retrieving documents.
        retriever (BM25Retriever): A retriever for retrieving relevant documents.
        pipeline (RetrieverQuestionGenerationPipeline): A pipeline for generating questions based on retrieved documents.
        question_generator (QuestionGenerator): A question generator for generating questions.
        reader (FARMReader): A reader for generating answers to the generated questions.

    Methods:
        add_documents: Adds documents to the document store.
        format_text: Formats the text into a list of dictionaries suitable for indexing.
        generate_questions: Generates questions and answers for the documents in the document store.
    """

    def __init__(self):
        """
        Initializes the ExamGenerator.

        It creates an ElasticsearchDocumentStore, a retriever, a question generator, and a reader.
        """
        self.document_store = ElasticsearchDocumentStore()
        self.retriever = None
        self.pipeline = None
        self.question_generator = QuestionGenerator()
        self.reader = FARMReader("deepset/roberta-base-squad2")

    def add_documents(self, documents):
        """
        Adds documents to the document store.

        Args:
            documents (list): A list of documents to be added to the document store.
        """
        self.document_store.delete_documents()
        self.document_store.write_documents(documents)

    @staticmethod
    def format_text(text):
        """
        Formats the given text into a list of dictionaries suitable for indexing.

        Args:
            text (str): The text to be formatted.

        Returns:
            list: A list of dictionaries, where each dictionary contains the formatted text as "content".
        """
        document = []
        for line in text.split('\n'):
            document.append({"content": line})
        return document

    def generate_questions(self):
        """
        Generates questions and answers for the documents in the document store.

        Returns:
            dict: A dictionary containing the generated questions as "questions" and the generated answers as "answers".
        """
        question_generation_pipeline = QuestionAnswerGenerationPipeline(
            self.question_generator,
            self.reader
        )
        for idx, document in enumerate(tqdm(self.document_store)):
            print(f" *** Generating questions and answers for document {idx} ***  {document.content[:50]}")
            results = question_generation_pipeline.run(documents=[document])
            
        return {'questions': results['queries'], 'answers': results['answers']}
