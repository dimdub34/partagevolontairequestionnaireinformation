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


def get_text_explanation():
    return u"Merci de répondre aux questions ci-dessous. Le traitement des " \
           u"réponses sera totalement anonyme."


