import datetime
import os
import unicodecsv as csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mptindicators.scorecard.models import Country, Section, Indicator

TMP_DIR = settings.TMP_DIR


def write_countries(path):

    path = os.path.join(path, 'countries.csv')

    with open(path, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ('code', 'name',
             'aggregate_score', 'in_law_score', 'in_practice_score',
             'findings', 'electoral_system'))

        for c in Country.objects.all().order_by('code'):
            row = (c.code, c.name,
                   c.aggregate_score, c.in_law_score, c.in_practice_score,
                   c.findings, c.electoral_summary)
            writer.writerow(row)


def write_sections(path):

    path = os.path.join(path, 'sections.csv')

    with open(path, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ('section_number', 'section_name',
             'subsection_number', 'subsection_name'))

        for s in Section.objects.all():
            writer.writerow((s.number, s.name, '', ''))
            for ss in s.subsections.all():
                writer.writerow((s.number, s.name, ss.number, ss.name))


def write_indicators(path):

    path = os.path.join(path, 'indicators.csv')

    with open(path, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ('number', 'name', 'section', 'subsection',
             'type', 'criteria', 'comment'))

        for i in Indicator.objects.all().select_related():
            row = (i.number, i.name,
                   i.subsection.number, i.subsection.section.number,
                   i.type, i.criteria, i.comment)
            writer.writerow(row)


def write_scores(path):

    path = os.path.join(path, 'scores.csv')

    with open(path, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ('number', 'name', 'section', 'subsection',
             'type', 'criteria', 'comment'))

        for i in Indicator.objects.all().select_related():
            row = (i.number, i.name,
                   i.subsection.number, i.subsection.section.number,
                   i.type, i.criteria, i.comment)
            writer.writerow(row)


class Command(BaseCommand):

    help = 'Create data archive and publish to S3'

    # def add_arguments(self, parser):
    #     parser.add_argument('path')

    def handle(self, *args, **options):

        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)

        now = datetime.date.today()
        archive_path = os.path.join(TMP_DIR, now.isoformat())

        if not os.path.exists(archive_path):
            os.mkdir(archive_path)

        write_countries(archive_path)
        write_sections(archive_path)
        write_indicators(archive_path)
        write_scores(archive_path)









"""
            writer = csv.writer(bffr)

            writer.writerow(
                ('indicator', 'question', 'type', 'score',
                 'section', 'section_name', 'subsection', 'subsection_name'))

            for score in country.indicator_scores.select_related():

                indicator = score.indicator
                subsection = indicator.subsection
                section = subsection.section

                row = (
                    indicator.number,
                    indicator.name,
                    indicator.get_type_display(),
                    score.score,
                    section.number,
                    section.name,
                    subsection.number,
                    subsection.name,
                )

                writer.writerow(row)

            content = bffr.getvalue()

        filename = 'indicators_{}.csv'.format(slugify(country.name))

        resp = HttpResponse(content, content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        return resp
"""