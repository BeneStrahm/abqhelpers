# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for ABAQUS Field and History Outputs
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
import regionToolset

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_time_points(model, name, start=0.0, end=1.0, increment=0.01):
    model.TimePoint(name=name, points=((start, end, increment),), )


def create_history_output_whole_model(
        model, name, stepName, timePoint, variables=PRESELECT):
    model.HistoryOutputRequest(
        name=name, createStepName=stepName, variables=variables,
        timePoint=timePoint)


def create_field_output_whole_model(
        model, name, stepName, timePoint, variables=PRESELECT):
    model.FieldOutputRequest(
        name=name, createStepName=stepName, variables=variables,
        timePoint=timePoint)


def get_predefined_field_variables_structural_analysis():
    return (('S', 'MISES', 'E', 'PE', 'PEEQ', 'PEMAG', 'EE', 'THE', 'U', 'RF', 'CF', 'SF', 'TF', 'CSTRESS', 'CDISP'))


def get_predefined_field_variables_thermal_analysis():
    return (('HFL', 'NT', 'RFL'))


def create_integrated_output_section(
        model, instance, sectionName, point, normal):
    """
    Create integrated output section at a given instance partioned by a datum plane. Currently only works for planes parallel to the coordinate system axes.
    :param model: ABAQUS model object
    :param instance: A String specifying the repository key of the instance.
    :param sectionName: A String specifying the name of the section.
    :param point: A tuple of three floats specifying the point on the section plane.
    :param normal: A tuple of three floats specifying the normal vector of the section plane.
    """
    # Get offset of section plane depending on it's orientation
    if not normal[0] == 0:
        offset = point[0]
    elif not normal[1] == 0:
        offset = point[1]
    elif not normal[2] == 0:
        offset = point[2]

    # Get all faces of the instance
    a = model.rootAssembly
    f = a.instances[instance].faces[:]
    faceSet = []

    # Create list with points of faces that are on the section plane
    # The pointOn attribute is used to create a list. Like this the faces can be
    # refound to create a set with all faces using findAt() and a tuple of the points.
    for myFace in f:
        if not normal[0] == 0:
            if myFace.pointOn[0][0] == offset:
                faceSet.append(myFace.pointOn[0])
        elif not normal[1] == 0:
            if myFace.pointOn[0][1] == offset:
                faceSet.append(myFace.pointOn[0])
        elif not normal[2] == 0:
            if myFace.pointOn[0][2] == offset:
                faceSet.append(myFace.pointOn[0])

    # Create set with faces that are on the section plane by point
    faces = f.findAt(tuple(faceSet))
    sFaces = a.Surface(side1Faces=faces, name=sectionName+'-f')

    # Convert set with faces to region
    s = sFaces.faces[:]
    region = regionToolset.Region(side1Faces=s)

    # Create integrated output section
    model.IntegratedOutputSection(
        name=sectionName, surface=region)


# def create_history_output_at_RP(model, referencePoint, stepName=None, variables=()):
#     # Get reference point
#     a = model.rootAssembly
#     regionDef = a.Set(referencePoints=(
#         referencePoint[1],), name="out_" + referencePoint[0].name + '_' + '_'.join(variables))

#     if not stepName:
#         stepName = model.steps.keys()[1]

#     # Create history output
#     model.HistoryOutputRequest(name=referencePoint[0].name + '_' + '_'.join(
#         variables), createStepName=stepName, variables=variables, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)


# def create_history_output_at_RP_force(model, referencePoint, stepName=None, variables=('CF1', 'CF2', 'CF3', 'CM1', 'CM2', 'CM3', )):
#     # Create history output
#     create_history_output_at_RP(
#         model, referencePoint, stepName=stepName, variables=variables)


# def create_history_output_at_RP_disp(model, referencePoint, stepName=None, variables=('U1', 'U2', 'U3', 'UR1', 'UR2', 'UR3', )):
#     # Create history output
#     create_history_output_at_RP(
#         model, referencePoint, stepName=stepName, variables=variables)


# def create_field_output_at_edge(model, instance, stepName=None, variables=()):
#     # Get edge
#     a = model.rootAssembly
#     print(instance)
#     e = a.instances[instance].edges[:]
#     regionDef = a.Set(edges=e, name='out_' + instance +
#                       '_' + '_'.join(variables))

#     if not stepName:
#         stepName = model.steps.keys()[1]

#     # Create field output
#     model.FieldOutputRequest(name=instance + '_' + '_'.join(
#         variables), createStepName=stepName, variables=variables, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)


# def create_field_output_at_reinforcement(model, instance, stepName=None, variables=('S', 'E', 'EE', 'PE')):
#     create_field_output_at_edge(
#         model, instance, stepName=stepName, variables=variables)


# def create_face_set_at_datum_plane(model, datumPlane, instance, point, normal, stepName=None, variables=('S', 'E', 'EE', 'PE')):
#     # Get coodinate of section plan
#     if not normal[0] == 0:
#         offset = point[0]
#     elif not normal[1] == 0:
#         offset = point[1]
#     elif not normal[2] == 0:
#         offset = point[2]

#     # Get all faces
#     a = model.rootAssembly
#     f = a.instances[instance].faces[:]
#     faceSets = []
#     faceSetsNames = []

#     # Create intermediate sets
#     for myFace in f:
#         if not normal[0] == 0:
#             if myFace.pointOn[0][0] == offset:
#                 faceSets.append(a.Set(faces=(
#                     f[myFace.index:myFace.index+1],), name='out_section_cut' + str(myFace.index)))
#                 faceSetsNames.append('out_section_cut' + str(myFace.index))
#         elif not normal[1] == 0:
#             if myFace.pointOn[0][1] == offset:
#                 faceSets.append(a.Set(faces=(
#                     f[myFace.index:myFace.index+1],), name='out_section_cut' + str(myFace.index)))
#                 faceSetsNames.append('out_section_cut' + str(myFace.index))
#         elif not normal[2] == 0:
#             if myFace.pointOn[0][2] == offset:
#                 faceSets.append(a.Set(faces=(
#                     f[myFace.index:myFace.index+1],), name='out_section_cut' + str(myFace.index)))
#                 faceSetsNames.append('out_section_cut' + str(myFace.index))

#     if faceSets:
#         print(faceSets)
#         # Merge intermediate and existing sets
#         a.SetByBoolean(name='out_' + datumPlane + '_' +
#                        instance, sets=faceSets, operation=UNION)

#         # Clean up intermediate sets
#         for faceSetName in faceSetsNames:
#             del a.sets[faceSetName]

#         return 'out_' + datumPlane


# def create_field_output_at_set(model, setName,  stepName=None, variables=()):
#     # Get Set
#     a = model.rootAssembly

#     if setName:
#         # print(setName)
#         for set in a.sets.keys():
#             # print(setName)
#             if setName in set:
#                 regionDef = a.sets[set]

#         # Create field output
#         if not stepName:
#             stepName = model.steps.keys()[1]

#         mdb.models['Concrete_beam_4_P_B'].FieldOutputRequest(setName + '_' + '_'.join(
#             variables), createStepName=stepName, variables=variables, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)


# def create_field_output_at_section(model, setName, stepName=None, variables=('S', 'MISES', 'E', 'EE', 'PE')):
#     create_field_output_at_set(
#         model, setName, stepName=stepName, variables=variables)
