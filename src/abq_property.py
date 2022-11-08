# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for ABAQUS Property
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      03.11.2022
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
import pickle
import numpy as np

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def import_from_material_library(libPath, modelName, matName):
    # load material library
    mat_lib_file = open(libPath, "r")
    mat_lib = pickle.load(mat_lib_file)

    # find matName in library
    for mat in mat_lib:
        if mat[2] == matName:
            matTuple = mat[4]

    # import to model
    from material import createMaterialFromDataString
    createMaterialFromDataString(
        modelName, matTuple["Vendor material name"], matTuple["version"], matTuple['Data'])


def create_homogenous_solid_section(model, sectionName, material, thickness=None):
    model.HomogeneousSolidSection(
        name=sectionName, material=material, thickness=thickness)


def create_circular_truss_section(model, sectionName, material, radius=1):
    model.TrussSection(name=sectionName, material=material,
                       area=np.pi*radius**2)


def assign_section(model, part, setName, sectionName):
    p = model.parts[part]
    region = p.sets[setName]
    p.SectionAssignment(region=region, sectionName=sectionName, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
