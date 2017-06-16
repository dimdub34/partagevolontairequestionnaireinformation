# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import sys
import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import partagevolontairequestionnaireinformationParams as pms
import partagevolontairequestionnaireinformationTexts as texts_PVQI
from client.cltgui.cltguiwidgets import WExplication


logger = logging.getLogger("le2m")


class DQuestionnaireInformation(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DQuestionnaireInformation, self).__init__(parent)

        self.defered = defered
        self.automatique = automatique

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.wexplication = WExplication(
            parent=self, text=texts_PVQI.get_text_explanation(), size=(600, 50))
        layout.addWidget(self.wexplication)

        gridlayout = QtGui.QGridLayout()
        layout.addLayout(gridlayout)

        label_q1 = QtGui.QLabel(
            u"L’affichage des prélèvements a-t-il modifié votre prélèvement ?")
        gridlayout.addWidget(label_q1, 0, 0)
        self.radio_group_q1 = QtGui.QButtonGroup()
        hlayout_q1 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.ECHELLE_AUGMENTATION.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q1.addButton(radio, k)
            hlayout_q1.addWidget(radio)
        hlayout_q1.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        gridlayout.addLayout(hlayout_q1, 0, 1)

        gridlayout.addWidget(QtGui.QLabel(u"Quelles en sont les raisons? "),
                             1, 0, 1, 2)
        self.enonces = [
            u"Je souhaitais avoir le même niveau de prélèvement que les autres",
            u"Je souhaitais augmenter mon gain",
            u"Je souhaitais diminuer les coûts de prélèvement",
            u"Le groupe a augmenté son prélèvement, j’ai dû modifier mon \n"
            u"prélèvement de façon à ne pas avoir de gain négatif"
        ]
        row_number = 2
        self.group_buttons = list()
        hlayouts = list()
        for i, e in enumerate(self.enonces):
            gridlayout.addWidget(QtGui.QLabel(e), row_number+i, 0)
            self.group_buttons.append(QtGui.QButtonGroup())
            hlayouts.append(QtGui.QHBoxLayout())
            for k, v in sorted(pms.ECHELLE_ACCORD.items()):
                radio = QtGui.QRadioButton(v)
                self.group_buttons[-1].addButton(radio)
                hlayouts[-1].addWidget(radio)
            hlayouts[-1].addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
            gridlayout.addLayout(hlayouts[-1], row_number+i, 1)

        row_number = gridlayout.rowCount()
        hlayout_autre = QtGui.QHBoxLayout()
        hlayout_autre.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        hlayout_autre.addWidget(QtGui.QLabel(u"Autre"))
        gridlayout.addLayout(hlayout_autre, row_number, 0)
        self.text_edit = QtGui.QTextEdit()
        self.text_edit.setFixedSize(600, 100)
        gridlayout.addWidget(self.text_edit, row_number, 1)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def accept(self):
        try:
            if self.radio_group_q1.checkedId() == -1:
                raise ValueError(u"Il y a au moins une question à "
                                 u"laquelle vous n'avez pas répondu")
            for bg in self.group_buttons:
                if bg.checkedId() == -1:
                    raise ValueError(u"Il y a au moins une question à "
                                     u"laquelle vous n'avez pas répondu")
        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, u"Attention", e.message)
            return
        else:
            reponses = dict()
            reponses["PVQI_modification_prelevement"] = \
                self.radio_group_q1.checkedId()
            variables = ["PVQI_meme_prelevement", "PVQI_augmenter_mon_gain",
                         "PVQI_diminuer_couts_prelevements",
                         "PVQI_eviter_gain_negatif"]
            for i, e in enumerate(self.enonces):
                reponses[variables[i]] = self.group_buttons[i].checkedId()
            reponses["PVQI_autre"] = self.text_edit.toPlainText()
            if not self.automatique:
                confirmation = QtGui.QMessageBox.question(
                    self, u"Confirmation", u"Vous confirmez vos réponses?",
                    QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                if confirmation != QtGui.QMessageBox.Yes:
                    return
            logger.info(u"Send back: {}".format(reponses))
            super(DQuestionnaireInformation, self).accept()
            self.defered.callback(reponses)

    def reject(self):
        pass


if __name__ == "__main__":
    app = QtGui.QApplication([])
    screen = DQuestionnaireInformation(None, 0, None)
    screen.show()
    sys.exit(app.exec_())

