#include "rbfblender.h"


MStatus initializePlugin( MObject obj ) {
    MStatus status;
    MFnPlugin plugin( obj, "rbfblender", "1.0", "Any");
    const MString pitrigName("rbfblender");

    status = plugin.registerNode( "rbfblender", RbfBlender::kNodeId, RbfBlender::creator, RbfBlender::initialize );
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

