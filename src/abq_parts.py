# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for ABAQUS Parts
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      28.09.2022
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


def import_3_d_parts(model, pathToFile, bodyNum=1, combine=True, mergeSolidRegions=True):
    acis = mdb.openAcis(pathToFile, scaleFromFile=OFF)
    partName = os.path.split(pathToFile)[1].split('.')[-2]
    for i in range(bodyNum):
        model.PartFromGeometryFile(name=partName + '-' + str(i), geometryFile=acis, combine=combine,
                                   mergeSolidRegions=mergeSolidRegions, dimensionality=THREE_D, type=DEFORMABLE_BODY)
