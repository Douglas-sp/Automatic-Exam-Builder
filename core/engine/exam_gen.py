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
        self.reader = FARMReader("deepset/roberta-base-squad2")

    def add_documents(self, documents):
        self.document_store.delete_documents()
        self.document_store.write_documents(documents)

    @staticmethod
    def format_text(text):
        document = []
        for line in text.split('\n'):
            document.append({"content": line})
        return document

    def generate_questions(self):
        question_generation_pipeline = QuestionAnswerGenerationPipeline(
            self.question_generator,
            self.reader
            )
        for idx, document in enumerate(tqdm(self.document_store)):
            print(f" *** Generating questions and answers for document {idx} ***  {document.content[:50]}")
            results = question_generation_pipeline.run(documents=[document])
            
        return { 'questions': results['queries'], 'answers': results['answers'] }
