# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for ABAQUS General model settings
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      16.12.2022
# Execution:    Import functions / collections (from pyLek.helpers import util)
# Status:       In Progress
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Sources
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
import os

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def set_physical_constants(model, absoluteZero=0, stefanBoltzmann=0):
    """
    Set physical constants for the ABAQUS model
    :param model: ABAQUS model object
    :param absoluteZero: Absolute zero temperature, defaults to 0  
    :param stefanBoltzmann: Stefan-Boltzmann constant, defaults to 0
    """
    model.setValues(absoluteZero=absoluteZero)
    model.setValues(stefanBoltzmann=stefanBoltzmann)
