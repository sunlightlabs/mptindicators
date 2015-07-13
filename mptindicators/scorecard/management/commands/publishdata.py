import datetime
import os
import shutil
import unicodecsv as csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mptindicators.scorecard.models import Country, Section, Indicator, IndicatorScore
from zipfile import ZipFile

TMP_DIR = settings.TMP_DIR
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')


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
            ('country', 'indicator', 'score', 'comment', 'sources'))

        for i in IndicatorScore.objects.all().select_related():
            row = (i.country_id, i.indicator_id,
                   i.score, i.comment, i.sources)
            writer.writerow(row)


class Command(BaseCommand):

    help = 'Create data archive and publish to S3'

    def handle(self, *args, **options):

        # get path stuff set up

        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)

        now = datetime.date.today()
        archive_path = os.path.join(TMP_DIR, now.isoformat())

        if not os.path.exists(archive_path):
            os.mkdir(archive_path)

        # write data

        write_countries(archive_path)
        write_sections(archive_path)
        write_indicators(archive_path)
        write_scores(archive_path)

        # copy Excel spreadsheet

        src_path = os.path.join(DATA_DIR, 'mpt-indicators.xls')
        dst_path = os.path.join(archive_path, 'mpt-indicators.xls')

        shutil.copyfile(src_path, dst_path)

        # zip it

        zip_path = os.path.join(TMP_DIR, 'mpt_data.zip')

        with ZipFile(zip_path, 'w') as zf:
            for filename in os.listdir(archive_path):
                zf.write(os.path.join(archive_path, filename), filename)


        # cleanup

        shutil.rmtree(archive_path)
