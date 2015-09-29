//=======================================================================
// Copyright 2015 Michal Krupa.
// Distributed under the MIT License.
// (See accompanying file LICENSE or copy at
//  http://opensource.org/licenses/MIT)
//=======================================================================


#include <maya/MFnPlugin.h>
#include "rbfblender.h"


MStatus initializePlugin( MObject obj ) {
    MStatus status;
    MFnPlugin plugin( obj, "rbfblender", "1.0", "Any");
    const MString rbfblenderName("rbfblender");

    status = plugin.registerNode( rbfblenderName, RbfBlender::kNodeId, RbfBlender::creator, RbfBlender::initialize, MPxNode::kDependNode);
    if (!status) {
                    status.perror("Failed to register node rbfblender");
                    return status;
	}
    return status;
}


MStatus uninitializePlugin( MObject obj) {
     MStatus status;
     MFnPlugin plugin( obj );

     status = plugin.deregisterNode( RbfBlender::kNodeId );
     return status;
}

