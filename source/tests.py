

import unittest
import maya.OpenMaya as om

import maya.standalone
maya.standalone.initialize()

import maya.cmds as cmds
import os

cmds.loadPlugin("rbfblender")


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        cmds.file(new=True, f=True)
        
    def create_rbfblender(self):
        try:
            node = cmds.createNode("rbfblender", n="blender")
            success = True
        except:
            success = False
        return success

    def test_node_creation(self):
        success = self.create_rbfblender()
        try:
            rbf_nodes = cmds.ls(type="rbfblender")
            if rbf_nodes:
                success = True
            else:
                success = False
        except:
            success = False
        self.assert_(success, "Failed to create the node.")

    def test_input_attribute(self):
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        rbf_nodes = cmds.ls(type="rbfblender")
        rbf_node = rbf_nodes[0]
        self.assert_(cmds.attributeQuery("input", n=rbf_node, ex=True), "Failed to get the input attribute")
        self.assert_(cmds.attributeQuery("output", n=rbf_node, ex=True), "Failed to get the output attribute")
        self.assert_(cmds.attributeQuery("poses", n=rbf_node, ex=True), "Failed to get the poses attribute")
        
        
        try:
            cmds.setAttr("blender.poses[0].poseInputs[0]", 1.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 1.0)
            success = True
        except:
            success = False
        self.assert_(success, "Failed to set the poses attribute")
    
    def test_output_attribute(self):
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.setAttr("blender.input[0]", .4)
            cmds.setAttr("blender.poses[0].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 0.5)
            cmds.setAttr("blender.poses[1].poseInputs[0]", 1.0)
            cmds.setAttr("blender.poses[1].poseName", "test", type="string")
            cmds.setAttr("blender.poses[1].poseValues[0]", 1.0)
            success = True
        except Exception, e:
            success = False
            print e
        self.assert_(success, "Failed to set the poses attribute")
        
        cmds.getAttr("blender.output[0]")
        
        cmds.setAttr("blender.input[0]", .0)
        cmds.getAttr("blender.output[0]")
        cmds.setAttr("blender.input[0]", 1)
        cmds.getAttr("blender.output[0]")
        cmds.setAttr("blender.input[0]", .5)
        cmds.getAttr("blender.output[0]")

    def test_multi_output_attribute(self):
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.setAttr("blender.input[0]", 1.0)
            cmds.setAttr("blender.input[1]", 0.0)
            cmds.setAttr("blender.input[2]", 0.0)
            cmds.setAttr("blender.poses[0].poseInputs[0]", 1.0)
            cmds.setAttr("blender.poses[0].poseInputs[1]", 0.0)
            cmds.setAttr("blender.poses[0].poseInputs[2]", 0.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 1.0)
            cmds.setAttr("blender.poses[0].poseValues[1]", 0.5)
            cmds.setAttr("blender.poses[0].poseValues[2]", 0.0)
            
            cmds.setAttr("blender.poses[1].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[1].poseInputs[1]", 1.0)
            cmds.setAttr("blender.poses[1].poseInputs[2]", 0.0)
            cmds.setAttr("blender.poses[1].poseName", "test", type="string")
            cmds.setAttr("blender.poses[1].poseValues[0]", 0.0)
            cmds.setAttr("blender.poses[1].poseValues[1]", 0.6)
            cmds.setAttr("blender.poses[1].poseValues[2]", 0.0)
            
            cmds.setAttr("blender.poses[2].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[2].poseInputs[1]", 0.0)
            cmds.setAttr("blender.poses[2].poseInputs[2]", 1.0)
            cmds.setAttr("blender.poses[2].poseName", "test", type="string")
            cmds.setAttr("blender.poses[2].poseValues[0]", 0.0)
            cmds.setAttr("blender.poses[2].poseValues[1]", 0.7)
            cmds.setAttr("blender.poses[2].poseValues[2]", 1.0)
            success = True
        except Exception, e:
            success = False
            print e
        self.assert_(success, "Failed to set the poses attribute")
        
        cmds.getAttr("blender.output[0]")
        cmds.getAttr("blender.output[1]")
        
        
        
if __name__ == '__main__':
    unittest.main()
