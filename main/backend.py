import pickle
import re
from datetime import datetime
from threading import Thread

import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from tika import parser


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


def parser_pdf_docx(pdf_file):
    result = {}
    experience = []
    education = []
    skills = []
    with open('models/RandomForest.pickle', 'rb') as f:
        model = pickle.load(f)
    raw = parser.from_file(pdf_file)

    for text in raw['content'].split('\n\n'):
        if text != '':
            if model.predict([text])[0] == 'Experience':
                experience.append(text)
            if model.predict([text])[0] == 'Education':
                education.append(text)
            if model.predict([text])[0] == 'Skills':
                skills.append(text)
    result['Experience'] = ' '.join(experience)
    result['Education'] = ' '.join(education)
    result['Skills'] = ' '.join(skills)
    result['Education'] = result['Education'].replace('Education', '')

    return result


def extract_experience(text):
    today = datetime.today()

    datem = '' + today.strftime('%B') + ' ' + str(today.year)
    text = text.replace('Present', datem)

    dates = re.findall('([a-zA-Z]{3,9}\s{1}[0-9]{4}\s{1}to\s{1}[a-zA-Z]{3,9}\s{1}[0-9]{4})', text)
    exp = 0.
    for d in dates:
        d = d.split(' to ')
        d1 = datetime.strptime(d[0], '%B %Y')
        d2 = datetime.strptime(d[1], '%B %Y')
        exp = exp + (d2 - d1).days / 365.2425

    return exp


def extract_NNP(sentence):
    tokenized = sent_tokenize(sentence)

    result = []
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            mwtokenizer = nltk.MWETokenizer(separator='')
            mwtokenizer.add_mwe(('C', '#'))
            mwtokenizer.add_mwe(('c', '#'))
            words = mwtokenizer.tokenize(words)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""skill: {(<JJ>*<NN>*<NNP>*)*<LS>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)

            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'skill'):
                result.append(' '.join([i[0] for i in subtree.leaves()]))
                for i in subtree.leaves():
                    result.append(i[0])

    except Exception as e:
        print(str(e))
    return result


#
# def extract_education(sentence):
#     tokenized = sent_tokenize(sentence)
#     print(sentence)
#
#     result = []
#     r = {}
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             mwtokenizer = nltk.MWETokenizer(separator='')
#             mwtokenizer.add_mwe(('C', '#'))
#             mwtokenizer.add_mwe(('c', '#'))
#             words = mwtokenizer.tokenize(words)
#             tagged = nltk.pos_tag(words)
#             chunkGram = r"""skill: {(<NNP|NN>+(<POS>)*<IN>(<NNP>)+)+}"""
#             chunkParser = nltk.RegexpParser(chunkGram)
#             chunked = chunkParser.parse(tagged)
#
#             for subtree in chunked.subtrees(filter=lambda t: t.label() == 'skill'):
#                 result.append(' '.join([i[0] for i in subtree.leaves()]).lower())
#                 # for i in subtree.leaves():
#                 #      result.append(i[0])
#
#     except Exception as e:
#         print(str(e))
#     with open('models/education.pickle', 'rb') as f:
#         education = pickle.load(f)
#     print(result)
#     educations = []
#     degrees = []
#     for degree in education.items():
#         for d in degree[1]:
#             for educ in result:
#                 if educ.find(d + ' ') != -1:
#                     educations.append(educ)
#                     degrees.append(degree[0])
#
#     r['education'] = list(set(educations))
#     r['degree'] = list(set(degrees))
#     return r
#
def extract_education(sentence):
    r = {}
    result = sent_tokenize(sentence)
    with open('models/education.pickle', 'rb') as f:
        education = pickle.load(f)
    educations = []
    degrees = []
    for degree in education.items():
        for d in degree[1]:
            for educ in result:
                if educ.find(d + ' ') != -1:
                    educations.append(educ)
                    degrees.append(degree[0])
                    break
    r['education'] = list(set(educations))
    r['degree'] = list(set(degrees))
    return r


def extract_skills(text):
    nnp = extract_NNP(text.lower())
    with open('models/skills.pickle', 'rb') as skills:
        dict = pickle.load(skills)
    return list(set(nnp).intersection(set(dict)))


def html_to_txt(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = " ".join(p.text for p in soup.find_all('p'))
    text2 = ' '.join(p.text for p in soup.find_all('li'))
    return text + text2


def calculate_similarity(resume_skills, job_skills):
    with open('models/similarity.pickle', 'rb') as f:

        sum = 0
        similarity = pickle.load(f)
        for skill1 in job_skills:
            max = 0
            for skill2 in resume_skills:

                try:
                    sim = similarity.wv.similarity(skill1, skill2)
                except:
                    sim = 0
                if sim > max:
                    max = sim
            sum = sum + max

        return sum / len(job_skills)
