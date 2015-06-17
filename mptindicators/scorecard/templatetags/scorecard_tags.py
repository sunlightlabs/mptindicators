from django import template

COLOR_CLASSES = ('one', 'two', 'three', 'four', 'five')


register = template.Library()

@register.simple_tag
def score_class(score):
    if score is None or score < 0:
        return 'no-score'
    return COLOR_CLASSES[min(int(score / 20), 4)]


@register.assignment_tag
def section_agg(country, section):
    return country.aggregates.get(section=section,
                                  subsection=None)


@register.assignment_tag
def subsection_agg(country, subsection):
    return country.aggregates.get(section=subsection.section,
                                  subsection=subsection)


@register.assignment_tag
def indicator_score(country, indicator):
    return country.indicator_scores.get(indicator=indicator)
