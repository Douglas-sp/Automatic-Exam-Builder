import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy

# Initialize NLP tools
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')

# Define Exam Generation Module
class ExamGenerator:
    def __init__(self, course_material):
        self.course_material = course_material
        self.questions = []

    def analyze_course_material(self):
        # Tokenize and analyze the course material
        tokenized_sentences = sent_tokenize(self.course_material)
        for sentence in tokenized_sentences:
            # Tokenize and lemmatize the words in the sentence
            tokens = word_tokenize(sentence.lower())
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords.words('english')]
            # Perform Named Entity Recognition (NER) and Part of Speech (POS) tagging
            doc = nlp(sentence)
            entities = [entity.text for entity in doc.ents]
            pos_tags = [token.pos_ for token in doc]
            # Add the analyzed sentence to a list of questions
            self.questions.append({'text': sentence, 'tokens': tokens, 'entities': entities, 'pos_tags': pos_tags})

    def generate_questions(self):
        # Generate questions from the analyzed course material
        for question in self.questions:
            # Select the appropriate question type based on the POS tags
            if 'VB' in question['pos_tags']:
                # Generate a fill-in-the-blank question
                verb_index = question['pos_tags'].index('VB')
                blank_question = question['text'][:verb_index] + '_____' + question['text'][verb_index+1:]
                self.questions.append({'text': blank_question, 'entities': question['entities']})
            elif 'NN' in question['pos_tags']:
                # Generate a multiple choice question
                noun_index = question['pos_tags'].index('NN')
                correct_answer = question['tokens'][noun_index]
                distractors = set(question['tokens']) - {correct_answer}
                distractors = list(distractors)[:3]
                distractors.append(correct_answer)
                distractors = sorted(distractors)
                answer_choices = ['A. '+distractors[0], 'B. '+distractors[1], 'C. '+distractors[2], 'D. '+distractors[3]]
                question_text = 'Which of the following is a ' + question['tokens'][noun_index] + '?\n' + '\n'.join(answer_choices)
                self.questions.append({'text': question_text, 'answer': 'D', 'entities': question['entities']})

    def filter_questions(self):
        # Filter the questions based on their entities
        filtered_questions = []
        for question in self.questions:
            if 'person' not in question['entities']:
                filtered_questions.append(question)
        self.questions = filtered_questions

    def format_exam(self):
        # Format the questions into an exam document
        exam_text = 'Exam\n\n'
        for i, question in enumerate(self.questions):
            exam_text += str(i+1) + '. ' + question['text'] + '\n\n'
        return exam_text
