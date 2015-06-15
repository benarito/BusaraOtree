import os

import dj_database_url
from boto.mturk.qualification import (LocaleRequirement,
                                      PercentAssignmentsApprovedRequirement,
                                      NumberHitsApprovedRequirement)

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


if os.environ.get('OTREE_PRODUCTION') in {None, '', '0'}:
    DEBUG = True
else:
    DEBUG = False

if os.environ.get('IS_OTREE_DOT_ORG') in {None, '', '0'}:
    ADMIN_PASSWORD = 'otree'
    # don't share this with anybody.
    # Change this to something unique (e.g. mash your keyboard),
    # and then delete this comment.
    SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'
else:
    ADMIN_PASSWORD = os.environ['OTREE_ADMIN_PASSWORD']
    SECRET_KEY = os.environ['OTREE_SECRET_KEY']

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}


ADMIN_USERNAME = 'admin'
AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')
ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'


INSTALLED_APPS = [
    'otree',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li><a href=mailto:bensonnjogu@gmail.com>Developer: Benson Njogu  </a></li>
    <li><a href="https://github.com/benarito/BusaraOtree" target="_blank">Source Code</a></li>
</ul>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

MTURK_WORKER_REQUIREMENTS = [
    LocaleRequirement("EqualTo", "US"),
    PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
    NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5)
]

# since workers on Amazon MTurk can return the hit
# we need extra participants created on the
# server.
# The following setting is ratio:
# num_participants_server / num_participants_mturk
MTURK_NUM_PARTICIPANTS_MULT = 2

SESSION_TYPE_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 10.00,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': {
        'keywords': ['easy', 'bonus', 'choice', 'study'],
        'title': 'Title for your experiment',
        'description': 'Description for your experiment',
        'frame_height': 500,
        'preview_template': 'global/MTurkPreview.html',
        'minutes_allotted_per_assignment': 60,
        'expiration_hours': 7*24, # 7 days
    },
}

SESSION_TYPES = [
    {
        'name': 'ultimatum',
        'display_name': "Ultimatum (randomized: strategy vs. direct response)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
    },

]


otree.settings.augment_settings(globals())
