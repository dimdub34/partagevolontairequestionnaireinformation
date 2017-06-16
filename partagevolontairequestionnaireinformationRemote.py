# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from client.cltremote import IRemote
import partagevolontairequestionnaireinformationParams as pms
from partagevolontairequestionnaireinformationGui import DQuestionnaireInformation


logger = logging.getLogger("le2m")


class RemotePVQI(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period

    def remote_display_decision(self):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            reponses = dict()
            reponses["PVQI_modification_prelevement"] = random.choice(
                pms.ECHELLE_AUGMENTATION.keys())
            variables = ["PVQI_meme_prelevement", "PVQI_augmenter_mon_gain",
                         "PVQI_diminuer_couts_prelevements",
                         "PVQI_eviter_gain_negatif"]
            for v in variables:
                reponses[v] = random.choice(pms.ECHELLE_ACCORD.keys())
            reponses["PVQI_autre"] = u"Texte simulation"
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, reponses))
            return reponses
        else:
            defered = defer.Deferred()
            ecran_decision = DQuestionnaireInformation(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen)
            ecran_decision.show()
            return defered
