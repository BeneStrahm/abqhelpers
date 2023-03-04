# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for postprocessing ABAQUS results
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


def create_path_along_point_list(session, name, point_list):
    session.Path(name=name, type=POINT_LIST, expression=point_list)


def create_xy_data_from_path(session, name, path, includeIntersections=False, projectOntoMesh=False, pathStyle=PATH_POINTS, shape=UNDEFORMED, labelType=TRUE_DISTANCE, removeDuplicateXYPairs=True, includeAllElements=False):
    session.XYDataFromPath(name=name, path=path, includeIntersections=includeIntersections, projectOntoMesh=projectOntoMesh, pathStyle=pathStyle,
                            shape=shape, labelType=labelType, removeDuplicateXYPairs=removeDuplicateXYPairs, includeAllElements=includeAllElements)


pth = session.paths['path889']
session.XYDataFromPath(name='XYData-2', path=pth, includeIntersections=False,
                       projectOntoMesh=False, pathStyle=PATH_POINTS, numIntervals=22,
                       projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE,
                       removeDuplicateXYPairs=True, includeAllElements=False)


point_list = ((0, 0, 0), (0, 0, 10), (0, 0, 20), (0, 0, 100))

create_path_along_point_list(session, 'path889', point_list)
