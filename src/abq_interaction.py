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
import regionToolset
import os
import pickle
import numpy as np

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_embedded_region(model, name, embeddedInstance, hostInstace):
    a = model.rootAssembly
    c = a.instances[embeddedInstance].cells[:]
    e = a.instances[embeddedInstance].edges[:]
    embeddedRegion = a.Set(edges=e, cells=c, name='m_' + embeddedInstance)

    c = a.instances[hostInstace].cells[:]
    e = a.instances[hostInstace].edges[:]
    hostRegion = a.Set(edges=e, cells=c, name='s_' + hostInstace)

    model.EmbeddedRegion(name="embedded_region_" + name,
                         embeddedRegion=embeddedRegion, hostRegion=hostRegion,
                         weightFactorTolerance=1e-06, absoluteTolerance=0.0,
                         fractionalTolerance=0.05, toleranceMethod=BOTH)


def create_mpc_beam_constraint(model, referencePoint, instance):
    # Get reference point
    a = model.rootAssembly
    controlPoint = a.Set(referencePoints=(
        referencePoint[1],), name="m_mpc_beam_" + referencePoint[0].name,)

    # Get corresponding face
    f = a.instances[instance].faces
    myFace = f.findAt(
        (referencePoint[0].xValue, referencePoint[0].yValue,
         referencePoint[0].zValue),)

    face = (f[myFace.index:myFace.index+1], )
    surface = a.Set(name="s_mpc_beam_" + referencePoint[0].name, faces=face)

    # Create MPC
    model.MultipointConstraint(
        name="mpc_beam_" + referencePoint[0].name, controlPoint=controlPoint,
        surface=surface, mpcType=BEAM_MPC, userMode=DOF_MODE_MPC, userType=0,
        csys=None)


def create_mpc_tie_constraint(model, referencePoint, instance):
    # Get reference point
    a = model.rootAssembly
    controlPoint = a.Set(referencePoints=(
        referencePoint[1],), name="m_mpc_tie_" + referencePoint[0].name,)

    # Get corresponding face
    f = a.instances[instance].faces
    myFace = f.findAt(
        (referencePoint[0].xValue, referencePoint[0].yValue,
         referencePoint[0].zValue),)

    face = (f[myFace.index:myFace.index+1], )
    surface = a.Set(name="s_mpc_tie_" + referencePoint[0].name, faces=face)

    # Create MPC
    model.MultipointConstraint(
        name="mpc_tie_" + referencePoint[0].name, controlPoint=controlPoint,
        surface=surface, mpcType=TIE_MPC, userMode=DOF_MODE_MPC, userType=0,
        csys=None)


def create_tie_surface_point(
        model, referencePoint, masterInstance, slaveInstance):
    a = model.rootAssembly

    # Get corresponding face (closest face within  tolerance)
    f = a.instances[masterInstance].faces
    myFace = f.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    face = (f[myFace[0][0].index:myFace[0][0].index+1], )
    master = a.Set(name="m_tie_" + referencePoint[0].name, faces=face)

    # Get slave point
    v = a.instances[slaveInstance].vertices
    myVertex = v.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    vertex = (v[myVertex[0][0].index:myVertex[0][0].index+1], )
    slave = a.Set(vertices=vertex, name="s_tie_" + referencePoint[0].name, )

    # Create Tie
    model.Tie(
        name="tie_" + referencePoint[0].name, master=master, slave=slave,
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON,
        thickness=ON)


def create_tie_surface_surface(
        model, referencePoint, masterInstance, slaveInstance):
    a = model.rootAssembly

    # Get corresponding face (closest face within tolerance)
    f = a.instances[masterInstance].faces
    myFace = f.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    face = (f[myFace[0][0].index:myFace[0][0].index+1], )
    master = a.Set(name="m_tie_" + referencePoint[0].name, faces=face)

    # Get slave surface (closest face within tolerance)
    f = a.instances[slaveInstance].faces
    myFace = f.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    face = (f[myFace[0][0].index:myFace[0][0].index+1], )
    slave = a.Set(name="s_tie_" + referencePoint[0].name, faces=face)

    # Create Tie
    model.Tie(
        name="tie_" + referencePoint[0].name, master=master, slave=slave,
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON,
        thickness=ON)


def create_coupling(
        model, referencePoint, controlInstance, slaveInstance, couplingType,
        u1=ON, u2=OFF, u3=OFF, ur1=OFF, ur2=OFF, ur3=OFF):
    a = model.rootAssembly

    # Get control point
    v = a.instances[controlInstance].vertices
    myVertex = v.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    vertex = (v[myVertex[0][0].index:myVertex[0][0].index+1], )
    controlPoint = a.Set(
        vertices=vertex, name="cp_coupling_" + referencePoint[0].name, )

    # Get corresponding face (closest face within  tolerance)
    f = a.instances[slaveInstance].faces
    myFace = f.getClosest(
        coordinates=((referencePoint[0].xValue,
                      referencePoint[0].yValue,
                      referencePoint[0].zValue),),
        searchTolerance=1)
    face = (f[myFace[0][0].index:myFace[0][0].index+1], )
    surface = a.Set(name="surf_coupling_" + referencePoint[0].name, faces=face)

    # Create Kinematic Coupling
    model.Coupling(
        name="coupling_" + str(couplingType).lower() + "_" +
        referencePoint[0].name, controlPoint=controlPoint, surface=surface,
        influenceRadius=WHOLE_SURFACE, couplingType=couplingType,
        localCsys=None, u1=u1, u2=u2, u3=u3, ur1=ur1, ur2=ur2, ur3=ur3)


def create_kinematic_coupling(
        model, referencePoint, controlInstance, slaveInstance, u1=ON, u2=OFF,
        u3=OFF, ur1=OFF, ur2=OFF, ur3=OFF):
    create_coupling(
        model, referencePoint, controlInstance, slaveInstance, KINEMATIC, u1=u1,
        u2=u2, u3=u3, ur1=ur1, ur2=ur2, ur3=ur3)


def create_distributing_coupling(
        model, referencePoint, controlInstance, slaveInstance, u1=ON, u2=OFF,
        u3=OFF, ur1=OFF, ur2=OFF, ur3=OFF):
    create_coupling(
        model, referencePoint, controlInstance, slaveInstance, DISTRIBUTING,
        u1=u1, u2=u2, u3=u3, ur1=ur1, ur2=ur2, ur3=ur3)


def create_film_condition(
        model, name, stepName, sFaces, filmCoeff, sinkTemperature,
        sinkAmplitude=''):
    """
    _summary_
    :param model: ABAQUS model object
    :param name: A String specifying the repository key.
    :param stepName: A String specifying the name of the step in which the interaction is created.
    :param sFaces: Set containing the faces where the film condition is applied
    :param filmCoeff:  A Float specifying the reference film coefficient value.
    :param sinkTemperature: A Float specifying the reference sink temperature. 
    :param sinkAmplitude: A String specifying the name of the Amplitude object that gives the variation of the sink temperature with time.
    """
    # Convert set with faces to region
    s = sFaces.faces[:]
    region = regionToolset.Region(side1Faces=s)

    # Create film condition
    model.FilmCondition(
        name='surf_film_' + name, createStepName=stepName, surface=region,
        definition=EMBEDDED_COEFF, filmCoeff=filmCoeff, filmCoeffAmplitude='',
        sinkTemperature=sinkTemperature, sinkAmplitude=sinkAmplitude,
        sinkDistributionType=UNIFORM, sinkFieldName='')


def create_radiation_to_ambient(
        model, name, stepName, sFaces, emissivity, ambientTemperature,
        ambientTemperatureAmp=''):
    """
    _summary_
    :param model: ABAQUS model object
    :param name: A String specifying the repository key.
    :param stepName: A String specifying the name of the step in which the interaction is created.
    :param sFaces: Set containing the faces where the film condition is applied
    :param emissivity: A Float specifying the emissivit
    :param ambientTemperature: A Float specifying the reference ambient temperature.
    :param ambientTemperatureAmp: A String specifying the name of the Amplitude object that gives the variation of the ambient temperature with time.
    """
    # Convert set with faces to region
    s = sFaces.faces[:]
    region = regionToolset.Region(side1Faces=s)

    # Create radiation to ambient condition
    model.RadiationToAmbient(
        name='surf_radi_' + name, createStepName=stepName, surface=region,
        radiationType=AMBIENT, distributionType=UNIFORM, field='',
        emissivity=emissivity, ambientTemperature=ambientTemperature,
        ambientTemperatureAmp=ambientTemperatureAmp)
