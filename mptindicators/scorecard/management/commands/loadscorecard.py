import re
from collections import defaultdict, namedtuple

import xlrd
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from mptindicators.scorecard.models import (
    Country, Section, Subsection, Indicator, IndicatorScore)

SECTION_RE = re.compile('(?:Section )?(\d).(\d)? (.*)')

#
# type definitions
#

CountryRecord = namedtuple('CountryRecord',
    ('name', 'column'))
SectionRecord = namedtuple('SectionRecord',
    ('section', 'subsection', 'title', 'row'))
QuestionRecord = namedtuple('QuestionRecord',
    ('number', 'text', 'description', 'comment', 'row', 'col', 'type'))
ScoreRecord = namedtuple('ScoreRecord',
    ('country', 'question', 'score', 'comment', 'sources', 'row', 'col'))


#
# data methods
#

def countries_iter(sheet):
    for col, cell in enumerate(sheet.row(1)):
        if col > 3:
            name = cell.value.split('-')[0].strip()
            yield CountryRecord(name, col)


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

            yield QuestionRecord(number, text, description, comment, row, col, type)
        except:
            pass


def sections_iter(sheet):
    col = 0
    for row, cell in enumerate(sheet.col(col)):
        match = SECTION_RE.match(cell.value)
        if match:
            (sec, subsec, title) = match.groups()
            title = title.strip()
            yield SectionRecord(int(sec), int(subsec) if subsec else None, title, row)


def get_score(sheet, country, question):

    col = country.column
    row = question.row

    score = sheet.cell(row, col).value
    comment = sheet.cell(row + 1, col).value.strip().encode('utf-8')
    sources = sheet.cell(row + 2, col).value.strip().encode('utf-8')

    return ScoreRecord(country, question, score, comment, sources, row, col)










class Command(BaseCommand):

    help = 'Import scorecard data from master spreadsheet'

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):

        book = xlrd.open_workbook(options['path'])
        sheet = book.sheets()[0]

        countries = list(countries_iter(sheet))
        questions = list(questions_iter(sheet))
        sections = list(sections_iter(sheet))

        def get_section(question):
            qsection = None
            for section in sections:
                if section.row > question.row:
                    break
                qsection = section
            return qsection


        #
        # load countries
        #

        print "loading countries..."

        Country.objects.all().delete()

        for record in countries:
            Country.objects.create(name=record.name,
                                   slug=slugify(record.name))

        #
        # load sections
        #

        print "loading sections and subsections..."

        Section.objects.all().delete()

        for record in sections:

            try:
                section = Section.objects.get(number=record.section)
            except Section.DoesNotExist:
                section = Section.objects.create(number=record.section)

            Subsection.objects.create(section=section,
                                      number=record.subsection,
                                      name=record.title)


        #
        # load indicators
        #

        print "loading indicators..."

        Indicator.objects.all().delete()

        for record in questions:

            ss = get_section(record)

            subsection = Subsection.objects.get(section__number=ss.section,
                                                number=ss.subsection)

            Indicator.objects.create(subsection=subsection,
                                     number=record.number,
                                     name=record.text,
                                     description=record.description,
                                     comment=record.comment,
                                     references='',
                                     type=record.type)

        #
        # load scores
        #

        print "loading indicator scores..."

        IndicatorScore.objects.all().delete()

        for country in countries:
            print '  {}'.format(country.name)
            for question in questions:
                score = get_score(sheet, country, question)

                value = None if score.score == '' else score.score

                iobj = Indicator.objects.get(number=question.number)
                cobj = Country.objects.get(name=country.name)

                IndicatorScore.objects.create(indicator=iobj,
                                              country=cobj,
                                              score=value,
                                              comment=score.comment,
                                              sources=score.sources)



