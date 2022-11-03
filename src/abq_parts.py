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
    part_list = []
    for i in range(bodyNum):
        if i == 0:
            model.PartFromGeometryFile(name=partName + '-' + str(i), geometryFile=acis, combine=combine,
                                       mergeSolidRegions=mergeSolidRegions, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        elif i > 0:
            model.PartFromGeometryFile(name=partName + '-' + str(i), geometryFile=acis, bodyNum=i+1, combine=combine,
                                       mergeSolidRegions=mergeSolidRegions, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        part_list.append(partName + '-' + str(i))
    return part_list


def create_datum_plane_by_principal(model, part, principalPlane, offset):
    p = model.parts[part]
    plane = p.DatumPlaneByPrincipalPlane(
        principalPlane=principalPlane, offset=offset)
    myID = plane.id
    return myID


def create_partition_by_datum_plane(model, part, id_plane):
    p = model.parts[part]
    c = p.cells[:]
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[id_plane], cells=c)


def create_Set_All_Cells(model, part, set_name):
    p = model.parts[part]
    c = p.cells[:]
    p.Set(cells=c, name=set_name)


def create_Set_Face(model, part, set_name, x, y, z):
    face = ()
    p = model.parts[part]
    f = p.faces
    myFace = f.findAt((x, y, z),)
    face = face + (f[myFace.index:myFace.index+1],)
    p.Set(faces=face, name=set_name)
    return myFace


def create_reference_point(x, y, z, model, setname):
    a = model.rootAssembly
    myRP = a.ReferencePoint(point=(x, y, z))
    r = a.referencePoints
    myRP_Position = r.findAt((x, y, z),)
    refPoints1 = (myRP_Position, )
    a.Set(referencePoints=refPoints1, name=setname)
    return myRP, myRP_Position
