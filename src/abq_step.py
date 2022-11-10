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

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_analysis_step(model, stepName, preStepName, initialInc, minInc, maxInc, incNumber, nlgeom):
    a = model.StaticStep(name=stepName, previous=preStepName,
                         initialInc=initialInc, maxInc=maxInc, minInc=minInc, nlgeom=nlgeom)
    a = model.steps[stepName].setValues(maxNumInc=incNumber)


def create_roller_support_at_RP(model, referencePoint, bcName='roller_', stepName="Initial"):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="roller_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(name=bcName + referencePoint[0].name, createStepName=stepName, region=region, u1=UNSET, u2=SET, u3=SET,
                         ur1=SET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)


def create_hinge_support_at_RP(model, referencePoint, bcName='hinge_', stepName="Initial"):
    # Get reference point
    a = model.rootAssembly
    region = a.Set(referencePoints=(
        referencePoint[1],), name="roller_" + referencePoint[0].name,)
    # Assign boundary condition
    model.DisplacementBC(name=bcName + referencePoint[0].name, createStepName=stepName, region=region, u1=SET, u2=SET, u3=SET,
                         ur1=SET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)


def create_prestress_temperature_at_(model, instance, magnitude, stepName='Prestress'):
    # Get edges
    a = model.rootAssembly
    e = a.instances[instance].edges[:]
    region = a.Set(edges=e, name='prestress_' + instance)
    model.Temperature(name='prestress_' + instance, createStepName=stepName, region=region,
                      distributionType=UNIFORM, crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(magnitude, ))
