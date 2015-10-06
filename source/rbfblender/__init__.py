import maya.cmds as cmds
# cmds.loadPlugin(r"D:\rbfblender\build\Release\rbfblender.mll")


def rbf_create_driver(driving_attributes, nodes_to_drive, attributes_to_drive, n=None):
    if n:
        node = cmds.createNode("rbfblender", n=n)
    else:
        node = cmds.createNode("rbfblender")

    for index in range(len(driving_attributes)):
        cmds.connectAttr(driving_attributes[index], node + ".input[{0}]".format(index))
    
    base_values = []
    attributes_list = []
    for node_to_d in nodes_to_drive:
        for at in attributes_to_drive:
            base_values.append(cmds.getAttr("{0}.{1}".format(node_to_d, at)))
            attributes_list.append("{0}.{1}".format(node_to_d, at))
    
    input_indices = cmds.getAttr("{0}.input".format(node), mi=True)
    for index in input_indices:
        cmds.setAttr("{0}.poses[0].poseInputs[{1}]".format(node, index), cmds.getAttr("{0}.input[{1}]".format(node, index)))
    
    for index in range(len(base_values)):
        cmds.setAttr("{0}.poses[0].poseValues[{1}]".format(node, index), base_values[index])
        
    for index in range(len(attributes_list)):
        cmds.connectAttr("{0}.output[{1}]".format(node, index), attributes_list[index])

        
def rbf_add_pose(rbfblender, clone_first=False):
    input_indices = cmds.getAttr("{0}.input".format(rbfblender), mi=True)
    output_indices = cmds.getAttr("{0}.output".format(rbfblender), mi=True)
    current_poses = cmds.getAttr("{0}.poses".format(rbfblender), mi=True)
    new_pose_index = current_poses[-1] + 1
    
    values = []
    for index in output_indices:
        if not clone_first:
            conn = cmds.listConnections("{0}.output[{1}]".format(rbfblender, index), s=False, d=True, p=True)
            if not conn:
                values.append(cmds.getAttr("{0}.output[{1}]".format(rbfblender, index)))
            else:
                values.append(cmds.getAttr(conn[0]))
        else:
            values.append(cmds.getAttr("{0}.poses[0].poseValues[{1}]".format(rbfblender, index)))
    
    for index in input_indices:
        cmds.setAttr("{0}.poses[{1}].poseInputs[{2}]".format(rbfblender, new_pose_index, index),
                     cmds.getAttr(rbfblender + ".input[{0}]".format(index)))
     
    for index in range(len(output_indices)):
         cmds.setAttr("{0}.poses[{1}].poseValues[{2}]".format(rbfblender, new_pose_index, output_indices[index]),
                     values[index])

def rbf_update_pose(rbfblender, reset_to_default=False):
    input_indices = cmds.getAttr("{0}.input".format(rbfblender), mi=True)
    output_indices = cmds.getAttr("{0}.output".format(rbfblender), mi=True)
    current_poses = cmds.getAttr("{0}.poses".format(rbfblender), mi=True)
    pose_index = cmds.getAttr("{0}.currentPoseIndex".format(rbfblender))
    if pose_index < 0:
        raise ValueError("No pose is reached right now.")
    
    values = []
    for index in output_indices:
        if not reset_to_default:
            conn = cmds.listConnections("{0}.output[{1}]".format(rbfblender, index), s=False, d=True, p=True)
            if not conn:
                values.append(cmds.getAttr("{0}.output[{1}]".format(rbfblender, index)))
            else:
                values.append(cmds.getAttr(conn[0]))
        else:
            values.append(cmds.getAttr("{0}.poses[0].poseValues[{1}]".format(rbfblender, index)))
    
    for index in input_indices:
        cmds.setAttr("{0}.poses[{1}].poseInputs[{2}]".format(rbfblender, pose_index, index),
                     cmds.getAttr(rbfblender + ".input[{0}]".format(index)))
     
    for index in range(len(output_indices)):
         cmds.setAttr("{0}.poses[{1}].poseValues[{2}]".format(rbfblender, pose_index, output_indices[index]),
                     values[index])
