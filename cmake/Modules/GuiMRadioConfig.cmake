find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GUIMRADIO GuiMRadio)

FIND_PATH(
    GUIMRADIO_INCLUDE_DIRS
    NAMES GuiMRadio/api.h
    HINTS $ENV{GUIMRADIO_DIR}/include
        ${PC_GUIMRADIO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GUIMRADIO_LIBRARIES
    NAMES gnuradio-GuiMRadio
    HINTS $ENV{GUIMRADIO_DIR}/lib
        ${PC_GUIMRADIO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/GuiMRadioTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GUIMRADIO DEFAULT_MSG GUIMRADIO_LIBRARIES GUIMRADIO_INCLUDE_DIRS)
MARK_AS_ADVANCED(GUIMRADIO_LIBRARIES GUIMRADIO_INCLUDE_DIRS)
