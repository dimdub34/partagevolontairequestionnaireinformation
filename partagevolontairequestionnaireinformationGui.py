# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import partagevolontairequestionnaireinformationParams as pms
from partagevolontairequestionnaireinformationTexts import trans_PVQI
import partagevolontairequestionnaireinformationTexts as texts_PVQI
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox


logger = logging.getLogger("le2m")


