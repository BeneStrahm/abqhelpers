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
import numpy as np

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_predefined_field_all_instances(
        model, fieldName, createStepName, magnitude):
    """
    Create a predefined field for all instances in the model
    :param model: ABAQUS model object
    :param fieldName: A String specifying the repository key.
    :param createStepName: A String specifying the name of the step in which the field is created.
    :param magnitude: A Float specifying the magnitude of the field.
    """
    a = model.rootAssembly
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            c = a.instances[key].cells[:]
            f = a.instances[key].faces[:]
            e = a.instances[key].edges[:]
            v = a.instances[key].vertices[:]
            region = a.Set(vertices=v, edges=e, faces=f, cells=c,
                           name='predefined_field_' + fieldName)
            model.Temperature(
                name=fieldName, createStepName=createStepName, region=region,
                distributionType=UNIFORM,
                crossSectionDistribution=CONSTANT_THROUGH_THICKNESS,
                magnitudes=(magnitude,))
