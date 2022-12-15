# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for ABAQUS Mesh
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


def seed_all_active_instances(model, size=10.0, deviationFactor=0.1, minSizeFactor=0.1):
    a = model.rootAssembly
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            # seed part instance
            a.seedPartInstance(
                regions=(a.instances[key],), size=size, deviationFactor=deviationFactor, minSizeFactor=minSizeFactor),

def seed_active_instance(model, instance, size=10.0, deviationFactor=0.1, minSizeFactor=0.1):
    a = model.rootAssembly
    # choose only active instances
    if a.instances[instance].ips != None:
        # seed part instance
        a.seedPartInstance(
            regions=(a.instances[instance],), size=size, deviationFactor=deviationFactor, minSizeFactor=minSizeFactor),

def assign_mesh_control_all_active_instances(model, elemTypes, elemShape=TET, technique=FREE, ):
    a = model.rootAssembly
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            c = a.instances[key].cells[:]
            # choose only instances with cells (e.g no linear elements)
            if c:
                a.setMeshControls(
                    regions=c, elemShape=elemShape, technique=technique)
                a.setElementType(regions=(c,), elemTypes=(elemTypes))

def generate_mesh_all_active_instances(model,):
    a = model.rootAssembly
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            # seed part instance
            a.generateMesh(
                regions=(a.instances[key],)),
