# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Helper functions for postprocessing ABAQUS results
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

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_path_along_point_list(session, pathName, point_list):
    """
    _summary_
    :param session: Abaqus session member
    :param pathName: A String specifying the repository key.
    :param point_list: A nested tuple containing the coordinates of the points along the path. For example, `point_list = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))`
    """
    session.Path(name=pathName, type=POINT_LIST, expression=point_list)


def create_xy_data_from_path(
        session, xydataName, pathName, variable, step, frame,
        includeIntersections=False, projectOntoMesh=False,
        pathStyle=PATH_POINTS, shape=UNDEFORMED, labelType=TRUE_DISTANCE,
        removeDuplicateXYPairs=True, includeAllElements=False):
    """
    This method creates an XYData object from path information.
    :param session: Abaqus session member
    :param xydataName: A String specifying the repository key.
    :param pathName: A String specifying the repository key.
    :param variable: A tuple of tuples containing the descriptions of variables for which to extract data along the path. The default value is the current variable. Each tuple specifies the following:Variable label: A String specifying the variable; for example, ‘U’.Variable output position: A SymbolicConstant specifying the output position. Possible values are ELEMENT_CENTROID, ELEMENT_FACE, ELEMENT_NODAL, GENERAL_PARTICLE, INTEGRATION_POINT, NODAL, WHOLE_ELEMENT, WHOLE_MODEL, WHOLE_PART_INSTANCE, and WHOLE_REGION.Refinement: A tuple specifying the refinement. If the refinement tuple is omitted, data are written for all components and invariants (if applicable). This element is required if the location dictionary (the following element in the tuple) is included. The refinement tuple contains the following:Type: A SymbolicConstant specifying the type of refinement. Possible values are INVARIANT and COMPONENT.Label: A String specifying the invariant or the component; for example, ‘Mises’ or ‘S22’.Location: An optional Dictionary specifying the location. The dictionary contains pairs of the following:A String specifying the category selection label.A String specifying the section point label.For example,`variable= (‘S’,INTEGRATION_POINT, ( (COMPONENT, ‘S22’ ), ), ) variable= ((‘S’,INTEGRATION_POINT, ((COMPONENT, ‘S11’ ), ), ), (‘U’,NODAL,((COMPONENT, ‘U1’),)),) variable= ((‘S’, INTEGRATION_POINT, ((INVARIANT, ‘Mises’ ), ), {‘shell < STEEL > < 3 section points >’:’SNEG, (fraction = -1.0)’, }), )`
    :param step: An Int identifying the step from which to obtain values. The default value is the current step.
    :param includeIntersections: A Boolean specifying whether to include X–Y data for the intersections between the path and element faces or edges. The default value is FALSE.
    :param projectOntoMesh: A Boolean to specify whether to consider the data points that do not lie on or inside the mesh. The default value is False.
    :param pathStyle: _description_, defaults to PATH_POINTS
    :param shape: A SymbolicConstant specifying the model shape to use. Possible values are UNDEFORMED and DEFORMED.
    :param labelType: A SymbolicConstant specifying the X-label type to use. Possible values are NORM_DISTANCE, SEQ_ID, TRUE_DISTANCE, TRUE_DISTANCE_X, TRUE_DISTANCE_Y, and TRUE_DISTANCE_Z.
    :param removeDuplicateXYPairs: A Boolean specifying whether to remove duplicate XY values from the final result. The default value is True.
    :param includeAllElements: A Boolean specifying whether to include elements which do not lie in the direction of the path. The default value is False.
    """
    session.XYDataFromPath(
        name=pathName + '_' + xydataName + '_' + str(step),
        path=session.paths[pathName],
        includeIntersections=includeIntersections,
        projectOntoMesh=projectOntoMesh, pathStyle=pathStyle, shape=shape,
        labelType=labelType, removeDuplicateXYPairs=removeDuplicateXYPairs,
        includeAllElements=includeAllElements, variable=variable, step=step,
        frame=frame)
    return pathName + '_' + xydataName + '_' + str(step)


def create_xy_data_from_field_nodal(
        session, xydataName, variable, nodeSets):
    """
    This method creates an XYData object from path information.
    :param session: Abaqus session member
    :param xydataName: A String specifying the repository key.
    :param variable: A tuple of tuples containing the descriptions of variables for which to extract data along the path. The default value is the current variable. Each tuple specifies the following:Variable label: A String specifying the variable; for example, ‘U’.Variable output position: A SymbolicConstant specifying the output position. Possible values are ELEMENT_CENTROID, ELEMENT_FACE, ELEMENT_NODAL, GENERAL_PARTICLE, INTEGRATION_POINT, NODAL, WHOLE_ELEMENT, WHOLE_MODEL, WHOLE_PART_INSTANCE, and WHOLE_REGION.Refinement: A tuple specifying the refinement. If the refinement tuple is omitted, data are written for all components and invariants (if applicable). This element is required if the location dictionary (the following element in the tuple) is included. The refinement tuple contains the following:Type: A SymbolicConstant specifying the type of refinement. Possible values are INVARIANT and COMPONENT.Label: A String specifying the invariant or the component; for example, ‘Mises’ or ‘S22’.Location: An optional Dictionary specifying the location. The dictionary contains pairs of the following:A String specifying the category selection label.A String specifying the section point label.For example,`variable= (‘S’,INTEGRATION_POINT, ( (COMPONENT, ‘S22’ ), ), ) variable= ((‘S’,INTEGRATION_POINT, ((COMPONENT, ‘S11’ ), ), ), (‘U’,NODAL,((COMPONENT, ‘U1’),)),) variable= ((‘S’, INTEGRATION_POINT, ((INVARIANT, ‘Mises’ ), ), {‘shell < STEEL > < 3 section points >’:’SNEG, (fraction = -1.0)’, }), )`
    :param nodeSets: A sequence of Strings specifying node sets or a String specifying a single node set.
    """
    # Access odb
    key = session.odbs.keys()[0]
    odb = session.odbs[key]

    # Create XYData
    xydata = session.xyDataListFromField(
        odb=odb, outputPosition=NODAL, variable=variable,
        nodeSets=nodeSets)

    xydata_name = str(xydata).split("\'")[1]

    session.xyDataObjects.changeKey(
        fromName=xydata_name, toName=nodeSets[0] + '_' + xydataName)

    return nodeSets[0] + '_' + xydataName


def create_xy_data_from_history_nodal(
        session, xydataName, outputVariableName, steps):
    """
    This method creates an XYData object from path information.
    :param session: Abaqus session member
    :param xydataName: A String specifying the repository key.
    :param outputVariableName: A String specifying the output variable from which the X–Y data will be read.
    :param steps: A sequence of Strings specifying the names of the steps from which data will be extracted.
    """
    # Access odb
    key = session.odbs.keys()[0]
    odb = session.odbs[key]

    # Create XYData
    session.XYDataFromHistory(name=xydataName, odb=odb,
                              outputVariableName=outputVariableName,
                              steps=steps)

    return xydataName


def write_xy_Report(session, xydataName, overwrite=True):
    """
    This method writes an XYData object to a report file.
    :param session: Abaqus session member
    :param xydataName: A String specifying the repository key.
    :param overwrite: A Boolean specifying whether to overwrite the file if it exists. Otherwise append results to file. The default value is True.
    """
    # Gather data
    x0 = session.xyDataObjects[xydataName]

    # Check if file exists
    if os.path.isfile(xydataName+'.rpt') and overwrite:
        os.remove(xydataName+'.rpt')

    # Export Report
    session.writeXYReport(fileName=xydataName+'.rpt', xyData=(x0, ))


def access_xy_data(session, xydata):
    """
    This method returns the data of an XYData object.
    :param session: Abaqus session member
    :param xydata: A String specifying the repository key.
    :return: A tuple containing the data of the XYData object.
    """
    # Gather data
    xy = session.xyDataObjects[xydata].data
    return xy
