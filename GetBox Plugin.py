# -*- coding: utf-8 -*-   
from pymol.cgo import * 
from pymol import cmd 
from random import randint
from pymol.vfont import plain
import sys
 
##############################################################################
# GetBox Plugin.py --  Draws a box surrounding a selection and gets box information
# This script is used to get box information for LeDock, Autodock Vina and AutoDock Vina. 
# Copyright (C) 2014 by Mengwu Xiao (Hunan University)      
#                                                         
# USAGES:  See function GetBoxHelp()        
# REFERENCE:  drawBoundingBox.py  written by  Jason Vertrees 
# EMAIL: mwxiao AT hnu DOT edu DOT cn
# Changes:  
# 2014-07-30 first version was uploaded to BioMS http://bioms.org/forum.php?mod=viewthread&tid=1234
# 2018-02-04 uploaded to GitHub https://github.com/MengwuXiao/Getbox-PyMOL-Plugin 
#            fixed some bugs: python 2/3 and PyMOL 1.x are supported;
#            added support to AutoDock;
#            added tutorials in English;
# NOTES: 
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.                                        
##############################################################################


def __init__(self):
	self.menuBar.addcascademenu('Plugin','GetBox Plugin','GetBox PyMOL Plugin',label = 'GetBox Plugin')
	self.menuBar.addmenuitem('GetBox Plugin', 'command','GetBoxHelp',label = 'Advanced usage',command = lambda s=self : GetBoxHelp())
	self.menuBar.addmenuitem('GetBox Plugin', 'command','AutoBox',label = 'Autodetect box',command = lambda s=self : autobox())
	self.menuBar.addmenuitem('GetBox Plugin', 'command','GetBox',label = 'Get box from selection (sele) ', command = lambda s=self : getbox())
	self.menuBar.addmenuitem('GetBox Plugin', 'command','Remove HETATM',label = 'Remove HETATM ', command = lambda s=self : rmhet())

 # to deal with print 
def printf(str):
    if sys.version < '3':
        exec ("print str")
    else:
        exec ("print(str)")
    
def GetBoxHelp():
    Usages = '''get latest plugin and tutorials at https://github.com/MengwuXiao/Getbox-PyMOL-Plugin

Usages:
this plugin is a simple tool to get box information for LeDock and Autodock Vina or other molecular docking soft. Using the following functions to get box is recommended.

* autobox [extending] (NOTES: solvent & some anions will be removed)
    this function autodetects box in chain A with one click of mouse, but sometimes it fails for too many ligands or no ligand
    e.g. autobox
    
* getbox [selection = (sele), [extending = 5.0]]
    this function creates a box that around the selected objects (residues or ligands or HOH or others). Selecting ligands or residues in the active cavity reported in papers is recommended
    e.g. getbox
    e.g. getbox (sele), 6.0
    
* resibox [Residues String, [extending = 5.0]]
    this function creates a box that arroud the input residues in chain A. Selecting residues in the active cavity reported in papers is recommended\n\
    e.g. resibox resi 214+226+245, 8.0
    e.g. resibox resi 234 + resn HEM, 6.0
    
* showbox [minX, maxX, minY, maxY, minZ, maxZ]
    this function creates a box based on the input axis, used to visualize box or amend box coordinate
    e.g. showbox 2,3,4,5,6,7
 
 * rmhet
 	remove HETATM, remove all HETATM in the screen
 	   
Notes:
* If you have any questions or advice, please do not hesitate to contact me (mwxiao AT hnu DOT edu DOT cn), thank you!'''

    printf (Usages)
    return
	
def showaxes(minX, minY, minZ):
	cmd.delete('axes')
	w = 0.5 # cylinder width 
	l = 5.0 # cylinder length
	obj = [
	CYLINDER, minX, minY, minZ, minX + l, minY, minZ, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
	CYLINDER, minX, minY, minZ, minX, minY + l, minZ, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
	CYLINDER, minX, minY, minZ, minX, minY, minZ + l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
	]
	cyl_text(obj,plain,[minX + l, minY, minZ - w],'X',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	cyl_text(obj,plain,[minX - w, minY + l , minZ],'Y',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	cyl_text(obj,plain,[minX-w, minY, minZ + l],'Z',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	cmd.load_cgo(obj,'axes')
	return
   
def showbox(minX, maxX, minY, maxY, minZ, maxZ):
    linewidth = 3.0
    minX = float(minX)
    minY = float(minY)
    minZ = float(minZ)
    maxX = float(maxX)
    maxY = float(maxY)
    maxZ = float(maxZ)
    showaxes(minX, minY, minZ)
    boundingBox = [
                   LINEWIDTH, float(linewidth),
        BEGIN, LINES,
        # x lines	 
        COLOR, 1.0, 0.0, 0.0, 	#red
        VERTEX, minX, minY, minZ,       #1
        VERTEX, maxX, minY, minZ,       #5
 
        VERTEX, minX, maxY, minZ,       #3
        VERTEX, maxX, maxY, minZ,       #7
 
        VERTEX, minX, maxY, maxZ,       #4
        VERTEX, maxX, maxY, maxZ,       #8
 
        VERTEX, minX, minY, maxZ,       #2
        VERTEX, maxX, minY, maxZ,       #6
        # y lines
		COLOR, 0.0, 1.0, 0.0, 	#green
		VERTEX, minX, minY, minZ,       #1
		VERTEX, minX, maxY, minZ,       #3
 
		VERTEX, maxX, minY, minZ,       #5
		VERTEX, maxX, maxY, minZ,       #7
 
		VERTEX, minX, minY, maxZ,       #2
		VERTEX, minX, maxY, maxZ,       #4
 
		VERTEX, maxX, minY, maxZ,       #6
		VERTEX, maxX, maxY, maxZ,       #8		
		# z lines
		COLOR, 0.0, 0.0, 1.0,		#blue
		VERTEX, minX, minY, minZ,       #1
		VERTEX, minX, minY, maxZ,       #2
 
		VERTEX, minX, maxY, minZ,       #3
		VERTEX, minX, maxY, maxZ,       #4
 
		VERTEX, maxX, minY, minZ,       #5
		VERTEX, maxX, minY, maxZ,       #6
 
		VERTEX, maxX, maxY, minZ,       #7
		VERTEX, maxX, maxY, maxZ,       #8
 
        END
    ]
    boxName = "box_" + str(randint(0, 10000))
    while boxName in cmd.get_names():
        boxName = "box_" + str(randint(0, 10000))
    cmd.load_cgo(boundingBox, boxName)
    SizeX = maxX - minX
    SizeY = maxY - minY
    SizeZ = maxZ - minZ
    CenterX =  (maxX + minX)/2
    CenterY =  (maxY + minY)/2
    CenterZ =  (maxZ + minZ)/2
    BoxCode = "BoxCode(" + boxName + ") = showbox %0.1f, %0.1f, %0.1f, %0.1f, %0.1f, %0.1f" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output LeDock input file
    LeDockBox = "*********LeDock Binding Pocket*********\n" + \
    "Binding pocket\n%.1f %.1f\n%.1f %.1f\n%.1f %.1f\n" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output AutoDock Vina input file
    VinaBox = "*********AutoDock Vina Binding Pocket*********\n" + \
    "--center_x %.1f --center_y %.1f --center_z %.1f --size_x %.1f --size_y %.1f --size_z %.1f\n" % (CenterX, CenterY, CenterZ, SizeX, SizeY, SizeZ)
    # output AutoDock box information 
    # add this function in 2016-6-25 by mwxiao
    AutoDockBox ="*********AutoDock Grid Option*********\n" + \
    "npts %d %d %d # num. grid points in xyz\n" % (SizeX/0.375, SizeY/0.375, SizeZ/0.375) + \
    "spacing 0.375 # spacing (A)\n" + \
    "gridcenter %.3f %.3f %.3f # xyz-coordinates or auto\n" % (CenterX, CenterY, CenterZ)

    printf(VinaBox)
    printf(AutoDockBox)
    printf(LeDockBox)
    printf(BoxCode)
    cmd.zoom(boxName)
    #cmd.show('surface')
    return boxName
        
def getbox(selection = "(sele)", extending = 5.0): 
	cmd.hide("spheres")
	cmd.show("spheres", selection)                                                                                                
	([minX, minY, minZ],[maxX, maxY, maxZ]) = cmd.get_extent(selection)
	minX = minX - float(extending)
	minY = minY - float(extending)
	minZ = minZ - float(extending)
	maxX = maxX + float(extending)
	maxY = maxY + float(extending)
	maxZ = maxZ + float(extending)
	cmd.zoom(showbox(minX, maxX, minY, maxY, minZ, maxZ))
	return
	
# remove ions
def removeions():
	cmd.select("Ions", "((resn PO4) | (resn SO4) | (resn ZN) | (resn CA) | (resn MG) | (resn CL)) & hetatm") 
	cmd.remove("Ions")
	cmd.delete("Ions")
	return
	
# autodedect box
def autobox(extending = 5.0):
	cmd.remove('solvent')
	removeions()
	cmd.select("ChainAHet","hetatm & chain A") #found error in pymol 1.8 change "chain a" to "chain A"
	getbox("ChainAHet", extending)
	return

# remove hetatm
def rmhet(extending = 5.0):
	cmd.select("rmhet","hetatm") 
	cmd.remove("rmhet")
	return

# getbox from cavity residues that reported in papers 
def resibox(ResiduesStr = "", extending = 5.0):
	cmd.select("Residues", ResiduesStr + " &  chain A")
	getbox("Residues", extending)
	return
	
cmd.extend ("getbox", getbox)
cmd.extend ("showbox", showbox)
cmd.extend ("autobox", autobox)
cmd.extend ("resibox", resibox)
cmd.extend ("GetBoxHelp", GetBoxHelp)
cmd.extend ("rmhet", rmhet)
