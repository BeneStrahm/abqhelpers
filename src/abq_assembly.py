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
    return i.name


def create_boolean_merge_assembly(model, instanceNames, name):
    a = model.rootAssembly
    instanceObjs = []
    for ele in instanceNames:
        instanceObjs.append(a.instances[ele])
    i = a.InstanceFromBooleanMerge(name=name, instances=(
        instanceObjs), keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)
    a.makeIndependent(instances=(i, ))
    return  i.name


def create_datum_plane_by_point_and_normal(model, point, normal):
    if not normal[0] == 0:
        principalPlane = YZPLANE
        offset = point[0]
    elif not normal[1] == 0:
        principalPlane = XZPLANE
        offset = point[1]
    elif not normal[2] == 0:
        principalPlane = XYPLANE
        offset = point[2]

    a = model.rootAssembly
    plane = a.DatumPlaneByPrincipalPlane(
        principalPlane=principalPlane, offset=offset)
    myID = plane.id
    return myID


def create_datum_plane_by_principal(model, part, principalPlane, offset):
    a = model.rootAssembly
    plane = a.DatumPlaneByPrincipalPlane(
        principalPlane=principalPlane, offset=offset)
    myID = plane.id
    return myID


def create_partition_by_datum_plane(model, instance, id_plane):
    a = model.rootAssembly
    c = a.instances[instance].cells[:]
    d = a.datums
    a.PartitionCellByDatumPlane(datumPlane=d[id_plane], cells=c, )
    return myID