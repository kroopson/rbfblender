

import unittest
import maya.OpenMaya as om

import maya.standalone
maya.standalone.initialize()

import maya.cmds as cmds
import os

cmds.loadPlugin("rbfblender")


class TestRbfBlender(unittest.TestCase):
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
        print "###################################################"
        print "TEST OUTPUT ATTRIBUTE"
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
        
    def test_single_pose(self):
        print "###################################################"
        print "TEST SINGLE POSE"
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.setAttr("blender.input[0]", .4)
            cmds.setAttr("blender.poses[0].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 0.5)
            success = True
        except Exception, e:
            success = False
            print e
        self.assert_(success, "Failed to set the poses attribute")
        
        cmds.getAttr("blender.output[0]")
        
    def test_duplicated_pose(self):
        print "###################################################"
        print "TEST DUPLICATED POSE"
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.setAttr("blender.input[0]", .4)
            cmds.setAttr("blender.poses[0].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 0.5)
            cmds.setAttr("blender.poses[1].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[1].poseName", "test", type="string")
            cmds.setAttr("blender.poses[1].poseValues[0]", 0.5)
            success = True
        except Exception, e:
            success = False
            print e
        self.assert_(success, "Failed to set the poses attribute")
        
        cmds.getAttr("blender.output[0]")
        
    def test_non_square_attribute(self):
        print "###################################################"
        print "TEST NON SQUARE ATTRIBUTE"
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.setAttr("blender.input[0]", 1.0)
            cmds.setAttr("blender.input[1]", 0.0)
            
            cmds.setAttr("blender.poses[0].poseInputs[0]", 1.0)
            cmds.setAttr("blender.poses[0].poseInputs[1]", 0.0)
            cmds.setAttr("blender.poses[0].poseInputs[2]", 0.0)
            cmds.setAttr("blender.poses[0].poseName", "test", type="string")
            cmds.setAttr("blender.poses[0].poseValues[0]", 1.0)
            cmds.setAttr("blender.poses[0].poseValues[1]", 0.5)
            
            
            cmds.setAttr("blender.poses[1].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[1].poseInputs[1]", 1.0)
            cmds.setAttr("blender.poses[1].poseInputs[2]", 0.0)
            cmds.setAttr("blender.poses[1].poseName", "test", type="string")
            cmds.setAttr("blender.poses[1].poseValues[0]", 0.0)
            cmds.setAttr("blender.poses[1].poseValues[1]", 0.6)
            
            
            cmds.setAttr("blender.poses[2].poseInputs[0]", 0.0)
            cmds.setAttr("blender.poses[2].poseInputs[1]", 0.0)
            cmds.setAttr("blender.poses[2].poseInputs[2]", 1.0)
            cmds.setAttr("blender.poses[2].poseName", "test", type="string")
            cmds.setAttr("blender.poses[2].poseValues[0]", 0.0)
            cmds.setAttr("blender.poses[2].poseValues[1]", 0.7)
            
            success = True
        except Exception, e:
            success = False
            print e
        self.assert_(success, "Failed to set the poses attribute")
        
        cmds.getAttr("blender.output[0]")
        cmds.getAttr("blender.output[1]")

    def test_multi_output_attribute(self):
        print "###################################################"
        print "TEST MULTI OUTPUT ATTRIBUTE"
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        cmds.setAttr("blender.output[0]", 0.0)
        cmds.setAttr("blender.output[1]", 0.0)
        cmds.setAttr("blender.output[2]", 0.0)
        
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
        cmds.getAttr("blender.output[2]")

    def test_cubes(self):
        print "###################################################"
        print "TEST CUBES"
        cube_test = cmds.polyCube()[0]

        cube_a = cmds.polyCube()[0]
        cube_b = cmds.polyCube()[0]
        cube_c = cmds.polyCube()[0]

        cmds.setAttr(cube_a + ".translate", -1, 0, 0)
        cmds.setAttr(cube_b + ".translate", 0, 0, 1)
        cmds.setAttr(cube_c + ".translate", 1, 0, 0)

        cmds.setAttr(cube_a + ".scale", 2, 1, 1)
        cmds.setAttr(cube_b + ".scale", 1, 2, 1)
        cmds.setAttr(cube_c + ".scale", 1, 1, 2)
        success = self.create_rbfblender()
        self.assert_(success, "Failed to create the node.")
        
        try:
            cmds.connectAttr(cube_test + ".translateX", "blender.input[0]")
            cmds.connectAttr(cube_test + ".translateZ", "blender.input[1]")
            
            cmds.connectAttr("blender.output[0]", cube_test + ".scaleX")
            cmds.connectAttr("blender.output[1]", cube_test + ".scaleY")
            cmds.connectAttr("blender.output[2]", cube_test + ".scaleZ")
            
            print "!! Creating pose 0"
            cmds.connectAttr(cube_a + ".translateX", "blender.poses[0].poseInputs[0]")
            cmds.connectAttr(cube_a + ".translateZ", "blender.poses[0].poseInputs[1]")
            cmds.connectAttr(cube_a + ".scaleX", "blender.poses[0].poseValues[0]")
            cmds.connectAttr(cube_a + ".scaleY", "blender.poses[0].poseValues[1]")
            cmds.connectAttr(cube_a + ".scaleZ", "blender.poses[0].poseValues[2]")
            
            print "!! Creating pose 1"
            cmds.connectAttr(cube_b + ".translateX", "blender.poses[1].poseInputs[0]")
            cmds.connectAttr(cube_b + ".translateZ", "blender.poses[1].poseInputs[1]")
            cmds.connectAttr(cube_b + ".scaleX", "blender.poses[1].poseValues[0]")
            cmds.connectAttr(cube_b + ".scaleY", "blender.poses[1].poseValues[1]")
            cmds.connectAttr(cube_b + ".scaleZ", "blender.poses[1].poseValues[2]")
            
            print "!! Creating pose 2"
            cmds.connectAttr(cube_c + ".translateX", "blender.poses[2].poseInputs[0]")
            cmds.connectAttr(cube_c + ".translateZ", "blender.poses[2].poseInputs[1]")
            cmds.connectAttr(cube_c + ".scaleX", "blender.poses[2].poseValues[0]")
            cmds.connectAttr(cube_c + ".scaleY", "blender.poses[2].poseValues[1]")
            cmds.connectAttr(cube_c + ".scaleZ", "blender.poses[2].poseValues[2]")
            
            success = True
        except Exception, e:
            success = False
            print e
            
        cmds.setAttr(cube_test + ".translate", -1, 0, 0)
        print "!!!!!!!!!!!!!!!!!!!!", cmds.getAttr(cube_test + ".scale")
        self.assert_( cmds.getAttr(cube_test + ".scale") == [(2, 1, 1)], "Bad result" + str(cmds.getAttr(cube_test + ".scale") ))
        
        cmds.setAttr(cube_test + ".translate", 0, 0, 1)
        self.assert_( cmds.getAttr(cube_test + ".scale") == [(1, 2, 1)], "Bad result")
        
        cmds.setAttr(cube_test + ".translate", 1, 0, 0)
        self.assert_( cmds.getAttr(cube_test + ".scale") == [(1, 1, 2)], "Bad result" + str(cmds.getAttr(cube_test + ".scale")))

    
    def test_output_set(self):
        print "###################################################"
        print "TEST OUTPUT SET"
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
        
        cmds.setAttr("blender.output[0]", 1.25)
        print "!!!!!!!!!!!!!!!!!", cmds.getAttr("blender.output[0]")
        # self.assert_(cmds.getAttr("blender.output[0]"))
        

if __name__ == '__main__':
    unittest.main()
