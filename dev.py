import re
from collections import defaultdict, namedtuple

import xlrd

SECTION_RE = re.compile('(?:Section )?(\d).(\d)? (.*)')

book = xlrd.open_workbook("data/GI MPT data form to Sunlight.xlsx")
sheet = book.sheets()[0]

#
# type definitions
#

Country = namedtuple('Country', ('name', 'column'))
Question = namedtuple('Question',
    ('number', 'text', 'description', 'comment', 'row', 'col'))
Score = namedtuple('Score',
    ('question', 'value', 'comment', 'sources', 'row', 'col'))


#
# data methods
#

def countries(sheet):
    for col, cell in enumerate(sheet.row(1)):
        if col > 3:
            name = cell.value.split('-')[0].strip()
            yield Country(name, col)


def questions(sheet):
    col = 1
    for row, cell in enumerate(sheet.col(col)):
        try:
            number = int(cell.value)
            text = sheet.cell(row, col + 1).value.strip()
            description = sheet.cell(row + 1, col + 1).value.strip()
            comment = sheet.cell(row + 2, col + 1).value.strip()
            yield Question(number, text, description, comment, row, col)
        except:
            pass


def sections(sheet):
    col = 2
    for row, cell in enumerate(sheet.col(col)):
        match = SECTION_RE.match(cell.value)
        if match:
            (sec, subsec, title) = match.groups()
            title = title.strip()
            yield (int(sec), int(subsec) if subsec else None, title, row)

# for country in countries(sheet):
#   print country

country_count = len(list(countries(sheet)))
for question in questions(sheet):
    print "{}. {}".format(question.number, question.text)
    for i in range(0, country_count):
        col = 4 + i
        name_cell = sheet.cell(1, col)
        name = name_cell.value.split('-')[0].strip()
        value_cell = sheet.cell(question.row, col)
        value = value_cell.value
        print "  {}: {}".format(name, value)

# print list(sections(sheet))


# for crange in sheet.merged_cells:
#   rlo, rhi, clo, chi = crange
#   if clo == 0 and chi == 1:
#       cell = sheet.cell(rlo, clo)
#       print rlo, cell.value, (rhi - rlo) / 3
