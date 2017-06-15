# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import partagevolontairequestionnaireinformationParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "partagevolontairequestionnaireinformation",
                             "locale")
    trans_PVQI = gettext.translation(
      "partagevolontairequestionnaireinformation", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_PVQI = lambda x: x  # if there is an error, no translation


def get_histo_vars():
    return ["PVQI_period", "PVQI_decision",
            "PVQI_periodpayoff",
            "PVQI_cumulativepayoff"]


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_PVQI(u"Explanation text")


def get_text_label_decision():
    return trans_PVQI(u"Decision label")


def get_text_summary(period_content):
    txt = trans_PVQI(u"Summary text")
    return txt


