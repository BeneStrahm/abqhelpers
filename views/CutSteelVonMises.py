# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Shows a cut trough an object in the Z Plane
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      04.08.2023
# Execution:    Copy to Abaqus CAE input
# Status:       Done
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
import displayGroupMdbToolset as dgm
import displayGroupOdbToolset as dgo

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
# 1) Load ODB
# 2) Switch to Vizualisation module
# 3) Copy code do Abaqus CAE

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

position = -41.00

# Change View
o = session.openOdb(name='Concrete_beam_4_P_B.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)

# Create Cut
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=ON)
session.viewports['Viewport: 1'].odbDisplay.setValues(
    viewCutNames=('Z-Plane', ), viewCut=ON)
session.viewports['Viewport: 1'].odbDisplay.viewCuts['Z-Plane'].setValues(
    position=position, showModelOnCut=True, showModelBelowCut=False,
    showModelAboveCut=False)

# Coloring by Material
cmap = session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()
session.viewports['Viewport: 1'].setColor(globalTranslucency=False)

# Select element set by Name
elementSets = ()
# Loop over all instances
for instanceName in o.rootAssembly.instances.keys():
    # Loop over element sets in instance
    for elementSet in o.rootAssembly.instances[instanceName].elementSets.keys():
        if 'EINBAUTEIL' in elementSet:
            elementSets += (instanceName + '.' + elementSet, )
        elif 'GEWINDESTAB' in elementSet:
            elementSets += (instanceName + '.' + elementSet, )
        elif 'MUTTER' in elementSet:
            elementSets += (instanceName + '.' + elementSet, )

# Replace display group
leaf = dgo.LeafFromElementSets(elementSets=elementSets)
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)

# Show von Mises Stresses
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=ELEMENT_CENTROID,
    refinement=(INVARIANT, 'Mises'),)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(
    plotState=(CONTOURS_ON_UNDEF, ))

# Set limits
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    maxAutoCompute=OFF, maxValue=560, minAutoCompute=OFF, minValue=460)

# Set colorbar
session.Spectrum(name="Yield Intensity", colors=('#32174F', '#FF1600', ))
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Yield Intensity', numIntervals=10)

# Setup Viewport
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    compass=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    annotations=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(state=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-80-*-*-p-*-*-*')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendTitle=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendDecimalPlaces=1, legendNumberFormat=FIXED)
