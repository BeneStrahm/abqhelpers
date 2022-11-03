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


def create_Assembly(model, part, instance, x=0, y=0, z=0):
    a = model.rootAssembly
    p = model.parts[part]
    a.Instance(name=instance, part=p, dependent=OFF)
    i = a.instances[instance]
    i.translate(vector=(x, y, z))
    return i


def create_boolean_merge_assembly(model, instanceNames, name):
    a = model.rootAssembly
    instanceObjs = []
    for ele in instanceNames:
        instanceObjs.append(a.instances[ele])
    i = a.InstanceFromBooleanMerge(name=name, instances=(
        instanceObjs), keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)
    a.makeIndependent(instances=(i, ))
