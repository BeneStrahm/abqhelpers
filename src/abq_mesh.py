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


def seed_all_active_instances(
        model, size=10.0, deviationFactor=0.1, minSizeFactor=0.1):
    a = model.rootAssembly
    for key in a.instances.keys():
        # choose only active instances
        if a.instances[key].ips != None:
            # seed part instance
            a.seedPartInstance(
                regions=(a.instances[key],),
                size=size, deviationFactor=deviationFactor,
                minSizeFactor=minSizeFactor),


def seed_active_instance(
        model, instances, size=10.0, deviationFactor=0.1, minSizeFactor=0.1):
    a = model.rootAssembly
    # choose only active instances
    for instance in instances:
        if a.instances[instance].ips != None:
            # seed part instance
            a.seedPartInstance(
                regions=(a.instances[instance],),
                size=size, deviationFactor=deviationFactor,
                minSizeFactor=minSizeFactor),


def seed_active_part(
        model, parts, size=10.0, deviationFactor=0.1, minSizeFactor=0.1):
    # choose only active instances
    for part in parts:
        if model.parts[part].ips != None:
            p = model.parts[part]
            p.seedPart(
                size=size, deviationFactor=deviationFactor,
                minSizeFactor=minSizeFactor)


def assign_mesh_control_all_active_instances(
        model, elemTypes, elemShape=TET, technique=FREE,):
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


def make_dependent_instance(model, instances):
    a = model.rootAssembly
    for instance in instances:
        a.makeDependent(instances=(a.instances[instance],))


def make_independent_instance(model, instances):
    a = model.rootAssembly
    for instance in instances:
        a.makeIndependent(instances=(a.instances[instance],))


def seed_edges_all_instances_in_bounding_box(
        model, xMin, yMin, zMin, xMax, yMax, zMax, size=10.0,
        deviationFactor=0.1, minSizeFactor=0.1):
    """
    This method creates a set of objects that lie within the specified bounding box.
    :param model: ABAQUS model object
    :param xMin: A float specifying the minimum *X*-boundary of the bounding box.
    :param yMin: A float specifying the minimum *Y*-boundary of the bounding box.
    :param zMin: A float specifying the minimum *Z*-boundary of the bounding box.
    :param xMax: A float specifying the maximum *X*-boundary of the bounding box.
    :param yMax: A float specifying the maximum *Y*-boundary of the bounding box.
    :param zMax: A float specifying the maximum *Z*-boundary of the bounding box.
    :param size: A Float specifying the desired global element size for the edges.
    :param deviationFactor: A Float specifying the deviation factor h/L, where is h the chordal deviation and L is the element length.
    :param minSizeFactor: A Float specifying the size of the smallest allowable element as a fraction of the specified global element size.
    """
    # get all instances
    a = model.rootAssembly

    # Empty lists for the different entity types
    e1 = []

    # Select entities across all entities by bounding box
    for key in a.instances.keys():

        # choose only active instances
        if a.instances[key].ips != None:
            e = a.instances[key].edges[:]
            e1 = e.getByBoundingBox(
                xMin, yMin, zMin, xMax, yMax, zMax)
            a.seedEdgeBySize(
                edges=e1, size=size, deviationFactor=deviationFactor,
                minSizeFactor=minSizeFactor, constraint=FINER)
