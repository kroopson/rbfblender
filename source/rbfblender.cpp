#include "rbfblender.h"


MObject RbfBlender::input;
MObject RbfBlender::output;
MObject RbfBlender::poses;
MObject RbfBlender::poseName;
MObject RbfBlender::poseInputs;
MObject RbfBlender::poseValues;

MObject RbfBlender::valueGuard;

MTypeId RbfBlender::kNodeId(0x0011827B);

RbfBlender::RbfBlender(){
}

RbfBlender::~RbfBlender(){
}

void* RbfBlender::creator(){
	return new RbfBlender();
}

double phiLinear(double r){
	return r;
}
//double PhiMultiquadratic(double radius){
//
//}

bool compareMIntArrays(MIntArray &first, MIntArray &second){
	if (first.length() != second.length()){
		return false;
	}

	for (unsigned int i = 0; i < first.length(); i++){
		if (first[i] != second[i]){
			return false;
		}
	}
	return true;
}

MStatus RbfBlender::recalculateDistancesMatrix(MDataBlock &data){
	MStatus stat;

	MPlug posesPlug(thisMObject(), poses);
	unsigned int numPoses = posesPlug.numElements();  // number of poses currently available
	if (numPoses == 0){  // quit if no poses created
		LOG_DEBUG_MESSAGE(MString("No poses found yet. Quitting"));
		return MStatus::kFailure;
	}

	// get the inputs plug and check if it's filled
	MPlug inputPlug(thisMObject(), input);
	MPlug outputPlug(thisMObject(), output);
	MIntArray inputIndices;
	MIntArray outputIndices;
	
	inputPlug.getExistingArrayAttributeIndices(inputIndices);
	if (inputIndices.length() == 0){
		LOG_DEBUG_MESSAGE(MString("No inputs found yet. Quitting"));
		return MStatus::kFailure;
	}

	outputPlug.getExistingArrayAttributeIndices(outputIndices);
	if (outputIndices.length() == 0){
		LOG_DEBUG_MESSAGE(MString("No outputs found yet. Quitting"));
		return MStatus::kFailure;
	}

	const unsigned int numInputs = inputIndices.length();  // count of input values
	const unsigned int numOutputs = outputIndices.length();  // count of output values
	// Start by resizing the matrixes and reseting all values on them
	distancesMatrix.fill(0.0);
	distancesMatrix.resize(numPoses, numPoses);
	valuesMatrix.fill(0.0);
	valuesMatrix.resize( numPoses, numOutputs);
	phiWeightsMatrix.fill(0.0);
	phiWeightsMatrix.resize( numPoses, numOutputs);

	//Eigen::VectorXd currentInputVector(inputIndices.length());
	Eigen::MatrixXd  poseInputsMatrix(numPoses, numInputs);

	// Create a matrix of pose inputs where each row is a vector of input assigned to a different pose.
	// I.e. 1, 0, 0 means first pose, 0, 1, 0 second and 0, 0, 1 is the third
	for (unsigned int poseIndex = 0; poseIndex < numPoses; poseIndex++){
		for (unsigned int i = 0; i < numInputs; i++){
			unsigned int indice = inputIndices[i];
			poseInputsMatrix(poseIndex, i) = posesPlug.elementByPhysicalIndex(poseIndex).child(1).elementByLogicalIndex(inputIndices[i]).asDouble();
		}
	}

	// Create a matrix of pose values where each row is a vector of values of the pose. That way in each column you'll have a values of one indice.
	// I.e. 1, 0, 0 is the first pose with value 1, .5, 0, Vector 0, 1, 0 second  with values 0, .6, 0 and 0, 0, 1 is the third with values 0, .7, 1.0
	// the matrix will look like this:
	// 1, .5, 0
	// 0, .6, 0
	// 0, .7, 1.0
	for (unsigned int poseIndex = 0; poseIndex < numPoses; poseIndex++){
		for (unsigned int i = 0; i < numOutputs; i++){
			unsigned int indice = outputIndices[i];
			valuesMatrix( poseIndex, i) = posesPlug.elementByPhysicalIndex(poseIndex).child(2).elementByLogicalIndex(outputIndices[i]).asDouble();
		}
	}

	bool zero_distance = false;
	// fill the distances matrix with distance from each pose input vector to all the other vectors.
	for (unsigned int poseIndex = 0; poseIndex < numPoses; poseIndex++){
		for (unsigned int i = 0; i < numPoses; i++){

			double distance = phiLinear((poseInputsMatrix.row(poseIndex) - poseInputsMatrix.row(i)).norm());
			distancesMatrix(i, poseIndex) = distance;
			// LOG_DEBUG_MESSAGE(MString("Distance is: ") + distance);
		}
	}
	
	// for each output multiply the column of values matrix by the inversed distances matrix.
	// This gives you weights for RBF function distances for this particular output.
	// Number of rows on weights vector equals the number of poses and number of columns equals the number of outputs
	for (unsigned int outputIndex = 0; outputIndex < numOutputs; outputIndex++){
		
		Eigen::MatrixXd weightsVector(0, 0);
		
		if (distancesMatrix.determinant() != 0){
			// weightsVector.resize(valuesMatrix.col(outputIndex).rows(), 1);
			weightsVector = distancesMatrix.inverse() * valuesMatrix.col(outputIndex);
		} else {
			weightsVector.resize(valuesMatrix.col(outputIndex).rows(), 1);
			weightsVector.fill(0.0f);
		}
		for (unsigned int rowIndex = 0; rowIndex < weightsVector.rows(); rowIndex++){
			phiWeightsMatrix(  rowIndex, outputIndex ) = weightsVector(rowIndex, 0);
		}
	}
	return MStatus::kSuccess;
}

MStatus RbfBlender::compute(const MPlug& plug, MDataBlock& data){
	MStatus stat;
	if (plug.isElement()){
		if (plug.array() == output){
			// DEBUG
			LOG_DEBUG_MESSAGE(MString("Computing output plug!") + plug.name());
		
			// Check if any poses available. If not just return 0.0
			MPlug poses(thisMObject(), poses);
			MDataHandle outputHandle = data.outputValue(plug);
			if (poses.numElements() == 0){
				// DEBUG
				// LOG_DEBUG_MESSAGE(MString("Missing any poses!"));
				outputHandle.setDouble(0.0);
				data.setClean(plug);
				return stat;
			}

			// get the logical index of this plug
			int currentPlugIndex = plug.logicalIndex();

			// get the current pose inputs to calculate distances from each pose.
			MPlug inputPlug(thisMObject(), input);
			MPlug posesPlug(thisMObject(), poses);
			MPlug outputsPlug(thisMObject(), output);
			MIntArray inputIndices;
			MIntArray outputIndices;
			
			inputPlug.getExistingArrayAttributeIndices(inputIndices);
			outputsPlug.getExistingArrayAttributeIndices(outputIndices);
			unsigned int outputPhysicalIndex;
			for (unsigned int outputIndex = 0; outputIndex < outputIndices.length(); outputIndex++){
				if (outputIndices[outputIndex] == plug.logicalIndex()){
					outputPhysicalIndex = outputIndex;
					// DEBUG
					// LOG_DEBUG_MESSAGE(MString("Found physical index:") + outputPhysicalIndex);
				}
			}

			if (poses.numElements() == 1){
				MIntArray indexes;
				poses.getExistingArrayAttributeIndices(indexes);
				// DEBUG
				// LOG_DEBUG_MESSAGE(MString("Only one pose!"));
				double value = poses.elementByLogicalIndex(indexes[0]).child(2).elementByLogicalIndex(currentPlugIndex).asDouble();
				outputHandle.setDouble(value);
				data.setClean(plug);
				return stat;
			}
			
			// Check if internal data needs to be recalculated
			// !data.isClean(valueGuard)
			MIntArray currentCalculatedIndices;
			plug.array().getExistingArrayAttributeIndices(currentCalculatedIndices);
			
			if (!data.isClean(valueGuard) || !compareMIntArrays(currentCalculatedIndices, lastCalculatedIndices)){
				// DEBUG
				LOG_DEBUG_MESSAGE(MString("Recalculating distances matrix"));
				MStatus result = recalculateDistancesMatrix(data);
				if (result == MStatus::kFailure){
					return MStatus::kFailure;
				}
				data.setClean(valueGuard);
				plug.array().getExistingArrayAttributeIndices(lastCalculatedIndices);
			}
			
			Eigen::MatrixXd currentInputsVector(inputPlug.numElements(), 1);
			for (unsigned int i=0; i < inputIndices.length(); i++){
				currentInputsVector(i, 0) = inputPlug.elementByLogicalIndex(inputIndices[i]).asDouble();
			}
			
			double result = 0.0;

			// Iterate all poses, get the distance from the pose to the current input vector and multiply it by the weight of the
			// pose. Weight matrix has been created with recalculateDistancesMatrix function.
			for (unsigned int poseIndex=0; poseIndex < poses.numElements(); poseIndex++){
				Eigen::MatrixXd poseInputsVector(inputPlug.numElements(), 1);
				for (unsigned int i=0; i < inputIndices.length(); i++){
					poseInputsVector(i, 0) = posesPlug.elementByPhysicalIndex(poseIndex).child(1).elementByLogicalIndex(inputIndices[i]).asDouble();
				}
				double distance = phiLinear((currentInputsVector - poseInputsVector).norm());
				double weight = phiWeightsMatrix( poseIndex, outputPhysicalIndex);
				result += distance * weight;
				// DEBUG
				// LOG_DEBUG_MESSAGE(MString("Distance from current is:") + distance);
				// LOG_DEBUG_MESSAGE(MString("Weight for current is:") + weight);
			}
			// DEBUG
			LOG_DEBUG_MESSAGE(MString("Result for this plug is:") + result);
			outputHandle.setDouble(result);
		}

		data.setClean(plug);
	}
	return stat;
}


MStatus RbfBlender::initialize(){
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	MStatus status;

	input = nAttr.create("input", "i", MFnNumericData::kDouble, 0.0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	nAttr.setArray(true);
	nAttr.setKeyable(false);

	poseName = tAttr.create("poseName", "pn", MFnData::kString, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	tAttr.setStorable(true);
	tAttr.setWritable(true);

	poseInputs = nAttr.create("poseInputs", "pi", MFnNumericData::kDouble, 0.0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	nAttr.setArray(true);
	nAttr.setWritable(true);
	nAttr.setStorable(true);

	poseValues = nAttr.create("poseValues", "pv", MFnNumericData::kDouble, 0.0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	nAttr.setArray(true);
	nAttr.setWritable(true);
	nAttr.setStorable(true);

	poses = cAttr.create("poses", "p", &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	cAttr.setArray(true);
	cAttr.addChild(poseName);
	cAttr.addChild(poseInputs);
	cAttr.addChild(poseValues);

	output = nAttr.create("output", "o", MFnNumericData::kDouble, 0.0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	nAttr.setArray(true);
	nAttr.setWritable(true);
	nAttr.setStorable(true);

	valueGuard = nAttr.create("valueGuard", "vg", MFnNumericData::kInt, 0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	nAttr.setStorable(false);
	nAttr.setHidden(true);
	nAttr.setWritable(false);

	addAttribute(input);
	addAttribute(poses);
	addAttribute(output);
	addAttribute(valueGuard);

	attributeAffects(input, output);

	attributeAffects(poseValues, output);
	attributeAffects(poseValues, valueGuard);
	attributeAffects(poseInputs, valueGuard);
	attributeAffects(poseInputs, output);

	return status;
}

void RbfBlender::postConstructor(){
}
