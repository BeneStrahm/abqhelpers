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
    i = a.InstanceFromBooleanMerge(
        name=name, instances=(instanceObjs),
        keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)
    a.makeIndependent(instances=(i, ))
    return i.name


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


def create_section_plane_by_point_and_normal(model, point, normal):
    myID = create_datum_plane_by_point_and_normal(model, point, normal)
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
    try:
        a.PartitionCellByDatumPlane(datumPlane=d[id_plane], cells=c, )
    except:
        print('Partitioning failed for instance: ' + instance)


def create_partition_by_section_plane(model, instance, id_plane):
    create_partition_by_datum_plane(model, instance, id_plane)


def create_set_by_bounding_box(
        model, entity_type, xMin, yMin, zMin, xMax, yMax, zMax, set_name):
    """
    This method creates a set of objects that lie within the specified bounding box.
    :param model: ABAQUS model object
    :param entity_type: A string specifying the type of the set. Possible values are 'v' for vertices, 'e' for edges, 'f' for faces and 'c' for cells.
    :param xMin: A float specifying the minimum *X*-boundary of the bounding box.
    :param yMin: A float specifying the minimum *Y*-boundary of the bounding box.
    :param zMin: A float specifying the minimum *Z*-boundary of the bounding box.
    :param xMax: A float specifying the maximum *X*-boundary of the bounding box.
    :param yMax: A float specifying the maximum *Y*-boundary of the bounding box.
    :param zMax: A float specifying the maximum *Z*-boundary of the bounding box.
    :param set_name: A string specifying the name of the set.
    """
    # get all instances
    a = model.rootAssembly

    # Empty lists for the different entity types
    v1 = []
    e1 = []
    f1 = []
    c1 = []

    # Select entities across all entities by bounding box
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            if entity_type == 'v':
                v = a.instances[key].vertices[:]
                v1.append(v.getByBoundingBox(
                    xMin, yMin, zMin, xMax, yMax, zMax))
            elif entity_type == 'e':
                e = a.instances[key].edges[:]
                e1.append(e.getByBoundingBox(
                    xMin, yMin, zMin, xMax, yMax, zMax))
            elif entity_type == 'f':
                f = a.instances[key].faces[:]
                f1.append(f.getByBoundingBox(
                    xMin, yMin, zMin, xMax, yMax, zMax))
            elif entity_type == 'c':
                c = a.instances[key].cells[:]
                c1.append(c.getByBoundingBox(
                    xMin, yMin, zMin, xMax, yMax, zMax))

    # Create sets from the selected entities
    if entity_type == 'v':
        s = a.Set(vertices=v1, name=set_name+'-v')
    elif entity_type == 'e':
        s = a.Set(edges=e1, name=set_name+'-e')
    elif entity_type == 'f':
        s = a.Set(faces=f1, name=set_name+'-f')
    elif entity_type == 'c':
        s = a.Set(cells=c1, name=set_name+'-c')

    return s
