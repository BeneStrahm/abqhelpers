# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  ** Add here short description **
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      04.03.2023
# Execution:    Set work-dir to this file & run script in ABAQUS CAE
# Status:       In Progress
# ------------------------------------------------------------------------------
# EXECUTION:
# 1. Open CMD in your working directory
# 2. Run script in ABAQUS CAE
# abaqus cae script=postprocessor.py
#
# TAIL LOGS:
# 1. Open CMD in your working directory
# 2. Use powershell to tail logs
# powershell Get-Content -Path abq_thermal_sim_slab.dat -WAIT
# powershell Get-Content -Path abq_thermal_sim_slab.msg -WAIT
# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
from driverUtils import *
from caeModules import *

# ------------------------------------------------------------------------------
# Install
# ------------------------------------------------------------------------------
# import custom libraries
import os
import imp
import re
import numpy as np

# path to abqhelpers
abq_path = "C:/Users/ac135564/GitHub/abqhelpers/"
abq_mat_lib = os.path.join(abq_path, "abaqus_plugins/MatLibrary.lib")

try:
    # in Python: add via relative import for type hints
    from abqhelpers.helpers import filemanager
except:
    # in Abaqus: add via imp for correct import
    filemanager = imp.load_source(
        'helpers.filemanager', os.path.join(abq_path, 'helpers/filemanager.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_postprocess
except:
    # in Abaqus: add via imp for correct import
    abq_postprocess = imp.load_source(
        'sec.abq_postprocess', os.path.join(abq_path, 'src/abq_postprocess.py'))


# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# Model
# ----------------

modelName = "abq_thermal_sim_slab"

# Load .odb
# ----------------

dir_path = os.getcwd()
odb_path = os.path.join(dir_path, modelName + ".odb")

# Open .odb
o = session.openOdb(name=odb_path)
session = session

# Set active viewport
session.viewports['Viewport: 1'].setValues(displayedObject=o)


# Create path
# ----------------

# Line w/ equally spaced points for output path
def line_with_equally_spaced_points_along_z_axis(x0, y0, z0, z1, nz):
    nx, ny, nz = (1, 1, nz)
    x = np.linspace(x0, y0, nx)           # x-coordinate
    y = np.linspace(y0, y0, ny)           # y-coordinate
    z = np.linspace(z0, z1, nz)      # z-coordinates
    # meshgrid - create 3D points along line
    xv, yv, zv = np.meshgrid(x, y, z)
    # array - flatten and transpose
    path_1 = np.vstack((xv.flatten(), yv.flatten(), zv.flatten())
                       ).T
    # tuple - convert to tuple
    return tuple(map(tuple, path_1))


path_1 = line_with_equally_spaced_points_along_z_axis(0, 0, -125, -75, 9)
path_2 = line_with_equally_spaced_points_along_z_axis(80, 0, -125, -75, 9)
path_3 = line_with_equally_spaced_points_along_z_axis(80, 80, -125, -75, 9)

abq_postprocess.create_path_along_point_list(session, 'path_1', path_1)
abq_postprocess.create_path_along_point_list(session, 'path_2', path_2)
abq_postprocess.create_path_along_point_list(session, 'path_3', path_3)

# Create XYData
# ----------------
xydata_1 = abq_postprocess.create_xy_data_from_path(
    session, 'NT11', 'path_1', ('NT11', NODAL,),
    0, includeIntersections=False, projectOntoMesh=False, pathStyle=PATH_POINTS,
    shape=UNDEFORMED, labelType=TRUE_DISTANCE, removeDuplicateXYPairs=True,
    includeAllElements=False)

abq_postprocess.write_xy_Report(session, xydata_1)


xydata_2 = abq_postprocess.create_xy_data_from_path(
    session, 'NT11', 'path_2', ('NT11', NODAL,),
    0, includeIntersections=False, projectOntoMesh=False, pathStyle=PATH_POINTS,
    shape=UNDEFORMED, labelType=TRUE_DISTANCE, removeDuplicateXYPairs=True,
    includeAllElements=False)

abq_postprocess.write_xy_Report(session, xydata_2, overwrite=True)


xydata_3 = abq_postprocess.create_xy_data_from_path(
    session, 'NT11', 'path_3', ('NT11', NODAL,),
    0, includeIntersections=False, projectOntoMesh=False, pathStyle=PATH_POINTS,
    shape=UNDEFORMED, labelType=TRUE_DISTANCE, removeDuplicateXYPairs=True,
    includeAllElements=False)

abq_postprocess.write_xy_Report(session, xydata_3, overwrite=True)
