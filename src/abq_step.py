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


def create_analysis_step(
        model, stepName, preStepName, initialInc, minInc, maxInc, incNumber,
        nlgeom):
    """
    Create a step with static loading
    :param model: ABAQUS model object
    :param stepName: A String specifying the repository key.
    :param preStepName: A String specifying the name of the previous step
    :param initialInc: A Float specifying the initial time increment
    :param minInc: A Float specifying the minimum time increment allowed
    :param maxInc: A Float specifying the maximum time increment allowed
    :param nlgeom: A Boolean specifying whether to allow for geometric nonlinearity
    """
    model.StaticStep(
        name=stepName, previous=preStepName, initialInc=initialInc,
        maxInc=maxInc, minInc=minInc, nlgeom=nlgeom)
    model.steps[stepName].setValues(maxNumInc=incNumber)
    return stepName


def create_analysis_step_with_temp(
        model, stepName, preStepName, timePeriod, maxNumInc, initialInc, minInc,
        maxInc, deltmx):
    """
    Create a step with temperature load
    :param model: ABAQUS model object
    :param stepName: A String specifying the repository key.
    :param preStepName: A String specifying the name of the previous step
    :param timePeriod: A Float specifying the total time period.
    :param maxNumInc: An Int specifying the maximum number of increments in a step.
    :param initialInc: A Float specifying the initial time increment
    :param minInc: A Float specifying the minimum time increment allowed
    :param maxInc: A Float specifying the maximum time increment allowed
    :param deltmx: A Float specifying the maximum temperature change to be allowed in an increment in a transient analysis
    """
    model.HeatTransferStep(
        name=stepName, previous=preStepName, timePeriod=timePeriod,
        maxNumInc=maxNumInc, initialInc=initialInc, minInc=minInc,
        maxInc=maxInc, deltmx=deltmx)
    return stepName


def create_roller_support_at_RP(
        model, referencePoint, bcName='roller_', stepName="Initial"):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="roller_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(
        name=bcName + referencePoint[0].name, createStepName=stepName,
        region=region, u1=UNSET, u2=SET, u3=SET, ur1=SET, ur2=UNSET, ur3=UNSET,
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)


def create_hinge_support_at_RP(
        model, referencePoint, bcName='hinge_', stepName="Initial"):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="hinge_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(
        name=bcName + referencePoint[0].name, createStepName=stepName,
        region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=UNSET, ur3=UNSET,
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)


def create_suppress_axial_rotation_at_edge(model, instance, stepName="Initial"):
    # Get edges
    a = model.rootAssembly
    e = a.instances[instance].edges[:]
    region = a.Set(edges=e, name='axial_rotation_' + instance)

    # Assign boundary condition
    model.DisplacementBC(name='axial_rotation_' + instance,
                         createStepName=stepName, region=region, u1=UNSET,
                         u2=UNSET, u3=UNSET, ur1=SET, ur2=UNSET, ur3=UNSET,
                         amplitude=UNSET, distributionType=UNIFORM,
                         fieldName='', localCsys=None)


def create_vertical_disp_at_RP(
        model, referencePoint, uz=1, bcName='load_disp_', stepName="Loading",
        amplitude=UNSET):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="load_disp_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(
        name=bcName + referencePoint[0].name, createStepName=stepName,
        region=region, u1=UNSET, u2=UNSET, u3=uz, ur1=UNSET, ur2=UNSET,
        ur3=UNSET, amplitude=amplitude, distributionType=UNIFORM, fieldName='',
        localCsys=None)


def create_horizontal_disp_at_RP(
        model, referencePoint, ux=1, bcName='load_disp_', stepName="Loading",
        amplitude=UNSET):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="load_disp_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(
        name=bcName + referencePoint[0].name, createStepName=stepName,
        region=region, u1=ux, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET,
        ur3=UNSET, amplitude=amplitude, distributionType=UNIFORM, fieldName='',
        localCsys=None)


def create_prestress_temperature_at_(
        model, instance, magnitude, stepName='Prestress', bcName='prestress_',
        amplitude=UNSET):
    # Get edges
    a = model.rootAssembly
    e = a.instances[instance].edges[:]
    region = a.Set(edges=e, name='prestress_' + instance)
    # if amplitude is None:
    model.Temperature(
        name=bcName + instance, createStepName=stepName,
        region=region, distributionType=UNIFORM,
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS,
        magnitudes=(magnitude,),
        amplitude=amplitude)


def create_prestress_temperature_at_solid(
        model, instance, magnitude, stepName='Prestress', amplitude=UNSET):
    # Get edges
    a = model.rootAssembly
    c = a.instances[instance].cells[:]
    region = a.Set(cells=c, name='prestress_' + instance)
    model.Temperature(
        name='prestress_' + instance, createStepName=stepName, region=region,
        distributionType=UNIFORM,
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS,
        magnitudes=(magnitude,), amplitude=amplitude)


def deactivate_boundary_condition(model, bcName, stepName):
    model.boundaryConditions[bcName].deactivate(stepName)


def reset_predefined_field_to_initial(model, fieldName, stepName):
    model.predefinedFields[fieldName].resetToInitial(stepName)


def create_tabular_amplitude(
        model, name, tabledata, timeSpan=STEP, smooth=SOLVER_DEFAULT):
    """
    Create a tabular amplitude
    :param model: ABAQUS model object
    :param name: A String specifying the repository key.
    :param tabledata: A sequence of Floats specifying the amplitude values.
    :param timeSpan: A SymbolicConstant specifying the time span of the amplitude, defaults to STEP
    :param smooth: The SymbolicConstant SOLVER_DEFAULT or a Float specifying the degree of smoothing, defaults to SOLVER_DEFAULT
    """
    model.TabularAmplitude(name=name, timeSpan=timeSpan, smooth=smooth,
                           data=tabledata)


def get_etk_EN_13501_2(t=14400, dt=600):
    """
    Uniform-temperature-time-curve for fire resistance tests according to EN 13501-2:2012
    :param t: time after the start of the fire in seconds, defaults to 14400 (240 minutes)
    :param dt:  interval of time in seconds, defaults to 300 (5 minutes)
    :return: time intervals, normalized temperature curve, maximum temperature after t seconds
    :rtype: tuple
    """
    t = np.arange(0, (t+dt)/60, dt/60)
    etk = 345 * np.log10(8 * t + 1) + 20
    etk_norm = etk / etk.max()
    etk_max = etk.max()
    return (t*60, etk_norm, etk_max)


def define_restart(
        model, stepName, numberIntervals=10, overlay=ON):
    """
    Requesting restart files
    :param model: ABAQUS model object
    :param stepName: A String specifying the name of the step.
    :param numberIntervals: An Int specifying the number of intervals per step, defaults to 10
    :param overlay: Specify whether the restart files are to be written over the existing files, defaults to ON
    """
    model.steps[stepName].Restart(
        frequency=0, numberIntervals=numberIntervals, overlay=overlay,
        timeMarks=OFF)
