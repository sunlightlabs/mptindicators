import re
from collections import defaultdict, namedtuple

import xlrd

SECTION_RE = re.compile('(?:Section )?(\d).(\d)? (.*)')

#
# type definitions
#

Country = namedtuple('Country',
    ('name', 'column'))
Section = namedtuple('Section',
    ('section', 'subsection', 'title', 'row'))
Question = namedtuple('Question',
    ('number', 'text', 'description', 'comment', 'row', 'col', 'type'))
Score = namedtuple('Score',
    ('country', 'question', 'score', 'comment', 'sources', 'row', 'col'))


#
# data methods
#

def countries_iter(sheet):
    for col, cell in enumerate(sheet.row(1)):
        if col > 3:
            name = cell.value.split('-')[0].strip()
            yield Country(name, col)


def questions_iter(sheet):
    col = 1
    for row, cell in enumerate(sheet.col(col)):
        try:
            number = int(cell.value)
            text = sheet.cell(row, col + 1).value.strip()
            description = sheet.cell(row + 1, col + 1).value.strip()
            comment = sheet.cell(row + 2, col + 1).value.strip()

            if text.startswith('In law'):
                type = 1
            elif text.startswith('In practice'):
                type = 2
            elif text.startswith('Open Question'):
                type = 3
            else:
                type = 0

            yield Question(number, text, description, comment, row, col, type)
        except:
            pass


def sections_iter(sheet):
    col = 0
    for row, cell in enumerate(sheet.col(col)):
        match = SECTION_RE.match(cell.value)
        if match:
            (sec, subsec, title) = match.groups()
            title = title.strip()
            yield Section(int(sec), int(subsec) if subsec else None, title, row)


def get_score(country, question):

    col = country.column
    row = question.row

    score = sheet.cell(row, col).value
    comment = sheet.cell(row + 1, col).value.strip().encode('utf-8')
    sources = sheet.cell(row + 2, col).value.strip().encode('utf-8')

    return Score(country, question, score, comment, sources, row, col)


book = xlrd.open_workbook("data/2015-05-13-final.xlsx")
sheet = book.sheets()[0]

countries = list(countries_iter(sheet))
questions = list(questions_iter(sheet))
sections = list(sections_iter(sheet))

print '{} countries'.format(len(countries))
print '{} questions'.format(len(questions))

for question in questions:
    qsection = None
    for section in sections:
        if section.row > question.row:
            break
        qsection = section
    print question.number, qsection

# for country in countries:
#     print '--- {} ---'.format(country.name)
#     for question in questions:
#         score = get_score(country, question)
#         print '    {}. {}'.format(question.number, question.text[:40])
#         print '        {} {}'.format(score.score, score.comment[:50])
