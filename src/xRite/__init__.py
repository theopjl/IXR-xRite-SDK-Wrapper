"""
xRite Python SDK Wrapper Package

This package provides Python wrappers for:
- i1Pro SDK for colorimetric measurements
- ColorChecker detection and color extraction using ArUco markers
"""

from xRite.i1pro_wrapper import (
    I1Pro,
    I1ProSDK,
    I1ProException,
    MeasurementMode,
    Illumination,
    Observer,
    I1ResultType,
    I1ConnectionStatusType,
    I1ButtonStatusType,
    I1DeviceEvent,
    SPECTRUM_SIZE,
    TRISTIMULUS_SIZE,
    DENSITY_SIZE,
)

from xRite.colorchecker_detector import (
    ColorCheckerDetector,
    COLORCHECKER_LAYOUTS,
    load_camera_params,
)

from xRite.colorchecker_template import (
    create_pdf_template,
    generate_aruco_marker,
    COLORCHECKER_SPECS,
    ARUCO_DICT,
    MARKER_SIZE_MM,
    MARKER_IDS,
)

__version__ = "1.0.0"
__all__ = [
    # i1Pro wrapper
    "I1Pro",
    "I1ProSDK",
    "I1ProException",
    "MeasurementMode",
    "Illumination",
    "Observer",
    "I1ResultType",
    "I1ConnectionStatusType",
    "I1ButtonStatusType",
    "I1DeviceEvent",
    "SPECTRUM_SIZE",
    "TRISTIMULUS_SIZE",
    "DENSITY_SIZE",
    # ColorChecker detector
    "ColorCheckerDetector",
    "COLORCHECKER_LAYOUTS",
    "load_camera_params",
    # ColorChecker template
    "create_pdf_template",
    "generate_aruco_marker",
    "COLORCHECKER_SPECS",
    "ARUCO_DICT",
    "MARKER_SIZE_MM",
    "MARKER_IDS",
]
