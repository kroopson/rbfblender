
#include <Eigen/Core>
#include <Eigen/LU>

#define EIGEN_DONT_ALIGN_STATICALLY
#define EIGEN_DONT_VECTORIZE
#define EIGEN_DISABLE_UNALIGNED_ARRAY_ASSERT

#ifndef RBRFBLENDER_H
#define RBRFBLENDER_H

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
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MVector.h>
#include <maya/MMatrix.h>

#include <maya/MQuaternion.h>
#include <maya/MAngle.h>

/* MACRO THAT DISPLAYS A MESSAGE IN CONSOLE ONLY IF THE PLUGIN HAS BEEN COMPILED IN Debug CONFIGURATION */
#ifdef _DEBUG	
#define LOG_DEBUG_MESSAGE(message)				\
MGlobal::displayInfo(MString("Debug: ") + message);
#endif
#ifndef _DEBUG
#define LOG_DEBUG_MESSAGE(message)
#endif


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
	static MObject poseName;
	static MObject poseInputs;
	static MObject poseValues;

	static MObject valueGuard;
private:
	Eigen::MatrixXd distancesMatrix;
	Eigen::MatrixXd valuesMatrix;
	Eigen::MatrixXd phiWeightsMatrix;

	MStatus recalculateDistancesMatrix(MDataBlock &data);
};

#endif
