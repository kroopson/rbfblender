//=======================================================================
// Copyright 2015 Michal Krupa.
// Distributed under the MIT License.
// (See accompanying file LICENSE or copy at
//  http://opensource.org/licenses/MIT)
//=======================================================================

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
#include <maya/MFnDependencyNode.h>

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
#define LOG_DEBUG_MESSAGE(message)				  \
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

	static MObject rbfKernel;
	static MObject blurParameter;  // Used for some kernels.

	// This attribute value is never used, however when it has dirty bit set to 1
	// the internal data - distancesMatrix, valuesMatrix and phiWeightsMatrix is recalculated.
	// It's a performance optimisation.
	static MObject valueGuard;

	virtual bool isPassiveOutput(const MPlug &plug) const;
private:
	MIntArray lastCalculatedIndices;

	Eigen::MatrixXd distancesMatrix;
	Eigen::MatrixXd valuesMatrix;
	Eigen::MatrixXd phiWeightsMatrix;

	MStatus recalculateDistancesMatrix(MDataBlock &data);
	double getPhi(double r);

	static double phiLinear(double r);
	static double phiMultiquadratic(double r, double blur);
	static double phiGaussian(double r, double blur);
	static double phiQubic(double r);
	static double phiThinPlate(double r);

	static bool compareMIntArrays(MIntArray &first, MIntArray &second);
};

#endif
