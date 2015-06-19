import csv
import re
from collections import defaultdict, namedtuple
from decimal import Decimal, ROUND_HALF_UP

import xlrd
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from mptindicators.scorecard.core import COUNTRIES
from mptindicators.scorecard.models import (
    Country, Section, Subsection, Indicator, IndicatorScore, Aggregate)

SECTION_RE = re.compile('(?:Section )?(\d).(\d)? (.*)')
SECTIONS = {
    1: 'Direct and Indirect Public Funding',
    2: 'Contribution and Expenditure Restrictions',
    3: 'Reporting and Public Disclosure',
    4: 'Third Party Actors',
    5: 'Monitoring and Enforcement',
}


#
# type definitions
#

CountryRecord = namedtuple('CountryRecord',
    ('name', 'column', 'code'))
SectionRecord = namedtuple('SectionRecord',
    ('section', 'subsection', 'title', 'row'))
QuestionRecord = namedtuple('QuestionRecord',
    ('number', 'text', 'description', 'comment', 'row', 'col', 'type'))
ScoreRecord = namedtuple('ScoreRecord',
    ('country', 'question', 'score', 'comment', 'sources', 'row', 'col'))


#
# data methods
#

# class DataSheet(object):
#     def __init__(self, sheet):
#         self.sheet = sheet

def countries_iter(sheet):
    for col, cell in enumerate(sheet.row(1)):
        if col > 3:
            name = cell.value.split('-')[0].strip()
            if name == 'Korea (Republic of)':
                name = 'South Korea'
            code = COUNTRIES.get(name, None)
            yield CountryRecord(name, col, code)


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


def get_aggregates(sheet):

    aggs = {}
    fields = ('composite', 'in_law', 'in_practice',
              '1', '1.1', '1.2',
              '2', '2.1', '2.2',
              '3', '3.1', '3.2',
              '4',
              '5', '5.1', '5.2')

    for row in range(1, 55):

        name = sheet.cell(row, 1).value.strip()
        data = {}

        for col in range(len(fields)):
            val = Decimal(sheet.cell(row, col + 2).value).quantize(
                Decimal('.01'), rounding=ROUND_HALF_UP)
            data[fields[col]] = val

        aggs[name] = data

    return aggs


def get_findings():
    findings = {}
    with open('data/findings.csv') as infile:
        dr = csv.DictReader(infile)
        findings = {r['Country'].strip(): r['Findings'].strip() for r in dr}
    return findings


class Command(BaseCommand):

    help = 'Import scorecard data from master spreadsheet'

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):

        book = xlrd.open_workbook(options['path'])
        data_sheet = book.sheets()[0]
        agg_sheet = book.sheets()[1]

        countries = list(countries_iter(data_sheet))
        questions = list(questions_iter(data_sheet))
        sections = list(sections_iter(data_sheet))

        def get_section(question):
            qsection = None
            for section in sections:
                if section.row > question.row:
                    break
                qsection = section
            return qsection

        #
        # load aggregates
        #

        print "loading findings..."
        findings = get_findings()

        #
        # load aggregates
        #

        print "loading aggregates..."
        aggregates = get_aggregates(agg_sheet)

        #
        # load countries
        #

        print "loading countries..."

        Country.objects.all().delete()

        for record in countries:
            aggs = aggregates.get(record.name)
            Country.objects.create(name=record.name,
                                   code=record.code,
                                   slug=slugify(record.name),
                                   aggregate_score=int(aggs['composite']),
                                   in_law_score=int(aggs['in_law']),
                                   in_practice_score=int(aggs['in_practice']),
                                   findings=findings.get(record.name, ''))

        #
        # load sections
        #

        print "loading sections and subsections..."

        Section.objects.all().delete()

        for record in sections:

            try:
                section = Section.objects.get(number=record.section)
            except Section.DoesNotExist:
                section = Section.objects.create(number=record.section,
                                                 name=SECTIONS[record.section])

            Subsection.objects.create(section=section,
                                      number=record.subsection,
                                      name=record.title)

        #
        # load section and subsection aggregates
        #

        print "loading section and subsection aggregates..."

        Aggregate.objects.all().delete()

        for country in Country.objects.all():
            for section in Section.objects.all():

                key = '{}'.format(section.number)
                val = aggregates[country.name][key]

                Aggregate.objects.create(country=country,
                                         section=section,
                                         subsection=None,
                                         score=int(val))

                for subsection in section.subsections.all():
                    key = '{}.{}'.format(section.number, subsection.number)
                    aggs = aggregates.get(country.name)
                    val = int(aggs[key]) if aggs and 'key' in aggs else None
                    Aggregate.objects.create(country=country,
                                             section=section,
                                             subsection=subsection,
                                             score=val)

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
                score = get_score(data_sheet, country, question)

                value = None if score.score == '' else score.score

                iobj = Indicator.objects.get(number=question.number)
                cobj = Country.objects.get(name=country.name)

                IndicatorScore.objects.create(indicator=iobj,
                                              country=cobj,
                                              score=value,
                                              comment=score.comment,
                                              sources=score.sources)
