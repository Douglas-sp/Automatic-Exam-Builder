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
    def __init__(self):
        self.document_store = ElasticsearchDocumentStore()
        self.retriever = None
        self.pipeline = None
        self.question_generator = QuestionGenerator()

    def add_documents(self, documents):
        self.document_store.write_documents(documents)

    @staticmethod
    def format_text(text):
        document = []
        for line in text.split('\n'):
            document.append({"content": line})
        return document

    def generate_questions(self):
        question_generation_pipeline = QuestionGenerationPipeline(self.question_generator)
        for idx, document in enumerate(self.document_store):
            print(f" *** Generating questions for document {idx} ***  {document.content[:50]}")
            result = question_generation_pipeline.run(documents=[document])
        return result
