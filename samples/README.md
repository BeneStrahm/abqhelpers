# 4_P_B_Concrete_Beam
Reinforced concrete beam under 4-point bending in ABAQUS.

## geometry
Contains a Rhino and Grasshopper file that allows to parametrically generate the 3D-Volume of the beam, load and support plates (.sat files) as well as related datum planes (.dp files containing a surface coordinate and it's nomal vector) and reference points (.rp files with coordinates and type(s) of the reference point (eg. mpc_beam))

All these are exported from Rhino using Grasshopper. The types of reference points, lated on used in the Python Script, are specified in Rhino using attributes.

## geometry/parts
Grasshopper is used to export the .sat, .dp and .rp files to the parts folder. 
