# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  ** Add here short description **
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      28.09.2022
# Execution:    Run script in ABAQUS CAE
# Status:       In Progress
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Install
# ------------------------------------------------------------------------------
if not "abqhelpers" in sys.path:
    sys.path.append("C:\\Users\\ac135564\\GitHub\\abqhelpers\\src")
    
# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from abaqus import *
from abaqusConstants import *
import regionToolset
import __main__
import part
import material
import section
import assembly
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import connectorBehavior
import odbAccess
from operator import add

import abq_parts

import os

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# Create Model
# ----------------
name = "Concrete_Frame_4_P_B"
model = mdb.Model(name=name)

# Create Parts
# ----------------

dir_path = os.getcwd()
dir_path = os.path.join(dir_path, "parts")

abq_parts.import_3_d_parts(model, os.path.join(
    dir_path, "concrete_beam.sat"))
abq_parts.import_3_d_parts(model, os.path.join(
    dir_path, "load_plate.sat"), bodyNum=2, combine=False, mergeSolidRegions=False)
abq_parts.import_3_d_parts(model, os.path.join(
    dir_path, "support_plate.sat"), bodyNum=2, combine=False, mergeSolidRegions=False)
