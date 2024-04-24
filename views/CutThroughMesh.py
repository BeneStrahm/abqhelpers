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

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
# 1) Switch to Mesh module
# 2) Copy code do Abaqus CAE

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

position = -41.00

# Change View
a = mdb.models['Concrete_beam_4_P_B'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)

# Create Cut
session.viewports['Viewport: 1'].assemblyDisplay.setValues(viewCut=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    activeCutName='Z-Plane', viewCut=ON)
session.viewports['Viewport: 1'].assemblyDisplay.viewCuts['Z-Plane'].setValues(
    position=position)

# Coloring
cmap = session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()
session.viewports['Viewport: 1'].setColor(globalTranslucency=True)
