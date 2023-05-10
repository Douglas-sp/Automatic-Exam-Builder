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

# Bloom's Taxonomy question templates
bloom_taxonomy = {
    "Remembering": [
        "What is {}?",
        "Who {}?",
        "When did {}?",
        "How many {}?",
        "List/describe {}."
    ],
    "Understanding": [
        "Explain in your own words, what is {}?",
        "What is the main idea of {}?",
        "Summarize {}.",
        "Give an example of {}.",
        "Compare and contrast {}."
    ],
    "Applying": [
        "How would you use {}?",
        "Solve the following problem related to {}.",
        "What would happen if {}?",
        "Demonstrate the use of {}.",
        "Construct/create {}."
    ],
    "Analyzing": [
        "What are the causes/effects of {}?",
        "How does {} relate to {}?",
        "What evidence supports {}?",
        "Compare and contrast the strengths and weaknesses of {}.",
        "What are the different components/parts of {}?"
    ],
    "Evaluating": [
        "Assess the validity of {}.",
        "Do you agree or disagree with {}? Justify your answer.",
        "What are the strengths and weaknesses of {}?",
        "Evaluate the impact of {}.",
        "What criteria would you use to judge {}?"
    ],
    "Creating": [
        "Design/imagine a new {}.",
        "Develop a plan to {}.",
        "Create a solution for {}.",
        "Invent a new way to {}.",
        "Write/compose a {}."
    ]
}

class ExamGenerator:
    def __init__(self):
        self.document_store = ElasticsearchDocumentStore()
        self.retriever = None
        self.pipeline = None
        self.question_generator = QuestionGenerator()

    def add_documents(self, documents):
        self.document_store.delete_documents()
        self.document_store.write_documents(documents)

    @staticmethod
    def format_text(text):
        document = []
        for line in text.split('\n'):
            document.append({"content": line})
        return document

    def generate_questions(self, taxonomy_level):
        question_generation_pipeline = QuestionGenerationPipeline(self.question_generator)
        question_templates = bloom_taxonomy.get(taxonomy_level)
        if not question_templates:
            print("Invalid taxonomy level!")
            return
        
        questions = []
        for idx, document in enumerate(self.document_store):
            print(f" *** Generating questions for document {idx} ***  {document.content[:50]}")
            results = question_generation_pipeline.run(documents=[document])
            for question in results['generated_questions'][0]['questions']:
                for template in question_templates:
                    questions.append(template.format(question))
        return questions



exam_generator = ExamGenerator()

documents = [
    {"content": "Document 1 content."},
    {"content": "Document 2 content."},
    # Add more documents as needed
]

exam_generator.add_documents(documents)

taxonomy_level = "Understanding"

questions = exam_generator.generate_questions(taxonomy_level)

print("Generated Questions:")
pprint(questions)
