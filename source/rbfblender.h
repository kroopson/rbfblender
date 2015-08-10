#ifndef RBFBLENDER
#define RBFBLENDER

#include <Eigen/Core>

#include <maya/MString.h>
#include <maya/MGlobal.h>

#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>

#include <maya/MVector.h>
#include <maya/MMatrix.h>

#include <maya/MQuaternion.h>
#include <maya/MAngle.h>
#include <maya/MFnPlugin.h>


class RbfBlender : public MPxNode{
public:
	// Standard plugin init stuff
	static MTypeId	kNodeId;
	RbfBlender();
	virtual ~RbfBlender();
	virtual MStatus compute(const MPlug& plug, MDataBlock& data);
	static MStatus initialize();
	static void* creator();
	virtual void postConstructor();

	// Attributes
	static MObject input;
	static MObject output;
	static MObject poses;
};

#endif