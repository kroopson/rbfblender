cmake_minimum_required(VERSION 2.8.0)

PROJECT(rbfblender)


SET (CMAKE_BUILD_TYPE RelWithDebInfo)
#SET (CMAKE_SHARED_LINKER_FLAGS "/export:initializePlugin /export:uninitializePlugin" ${CMAKE_SHARED_LINKER_FLAGS_INIT} $ENV{LDFLAGS}
 #    CACHE STRING "Flags used by the linker during the creation of dll's.")


LINK_DIRECTORIES("${MAYA_DIR}/lib")
INCLUDE_DIRECTORIES("${MAYA_DIR}/include")
INCLUDE_DIRECTORIES("${EIGEN_DIR}")

ADD_DEFINITIONS(-D REQUIRE_IOSTREAM)
ADD_DEFINITIONS(-D _BOOL)

SET(LIBRARY source/pluginSetup.cpp source/rbfblender.cpp source/rbfblender.h)

ADD_LIBRARY(rbfblender SHARED ${LIBRARY})

IF(WIN32)
    ADD_DEFINITIONS(-D NT_PLUGIN)
	TARGET_LINK_LIBRARIES(rbfblender Foundation.lib;OpenMaya.lib;OpenMayaUI.lib;OpenMayaAnim.lib)
    SET_TARGET_PROPERTIES(rbfblender PROPERTIES LINK_FLAGS "/export:initializePlugin /export:uninitializePlugin" SUFFIX ".mll")
    SET(MAYAPY_BIN mayapy.exe)
    ADD_CUSTOM_COMMAND(
    TARGET rbfblender
    POST_BUILD
    COMMAND set MAYA_PLUG_IN_PATH=$(OutDir)&& ${MAYA_DIR}/bin/${MAYAPY_BIN} ${CMAKE_CURRENT_LIST_DIR}/source/tests.py
    )
ELSE()
	ADD_DEFINITIONS(-fPIC)
	ADD_DEFINITIONS(-D LINUX)
	SET_TARGET_PROPERTIES(rbfblender PROPERTIES PREFIX "")
	TARGET_LINK_LIBRARIES(rbfblender libFoundation.so;libOpenMaya.so;libOpenMayaUI.so;libOpenMayaAnim.so)
    SET(MAYAPY_BIN mayapy)
    ADD_CUSTOM_COMMAND(
    TARGET rbfblender
    POST_BUILD
    COMMAND "${MAYA_DIR}/bin/${MAYAPY_BIN} ${CMAKE_CURRENT_LIST_DIR}/source/tests.py"
    )
ENDIF()



