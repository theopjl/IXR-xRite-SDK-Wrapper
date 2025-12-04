/*******************************************************************************
* Copyright (c) 2003-2014 X-Rite Inc.  All Rights Reserved.
*
* i1Pro.h is part of the i1Pro SDK.
*
* THIS FILE CANNOT BE REDISTRIBUTED in source code (or human readable) form,
* it cannot be modified, and it is only provided to compile applications
* for use with i1Pro hardware products.
*
* THIS SOFTWARE IS PROVIDED BY X-RITE ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL X-RITE BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
* THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************/

/* This file contains documentation for Doxygen */

/**
@mainpage i1Pro API Reference
@author X-Rite Inc.
@version 4.2
@date 2003-2014


@section intro Introduction
This API provides high-level methods to access the i1Pro family of USB devices. 
The interface is declared in ANSI C99. This means the types passed between an 
application and the SDK are basic C-types (float, long, char, etc) and all 
strings must be null-terminated. The interface is const-correct, meaning that 
input arguments marked as const will not be modified (input only) and output 
parameters marked as const, must not be modified.

The SDK is implemented in a stateful way, which means an application programmer 
must first set the desired measurement kind (by calling I1_SetOption) and only 
after that can they trigger a measurement and fetch the resulting data.


@section support Support
If you have any requests or comments about the SDK, please contact us via email 
at devsupport@xrite.com. Please be sure to indicate the product, version and 
category (e.g. SDK) you need help with.


@section library Library
The i1Pro library contains software that interfaces with the i1Pro.

@subsection library_devices Supported instruments
This SDK supports these i1Pro revisions:
  - i1Pro RevE (Revision E), aka i1Pro2
  - i1Pro (Revision A, B, C, D)

@subsection library_win Windows
These files are necessary to build an application that uses the i1Pro:
  - i1Pro.h
  - MeasurementConditions.h
  - i1Pro.lib for win32 or i1Pro64.lib for win64
  - i1Pro.dll for win32 or i1Pro64.dll for win64

The i1Pro.dll (or i1Pro64.dll for 64 bit architecture) is necessary to execute 
the application and must be included in the same folder as the application or 
placed in the DLL search path.

@subsection library_mac Mac OS X
These files are necessary to build an application that uses the i1Pro:
  - i1Pro.h
  - MeasurementConditions.h
  - i1Pro.framework

The i1Pro.framework must be put in the Frameworks folder inside the 
application bundle. It is compiled for i386 and x86_64.


@section driver USB Driver
The i1Pro family of instruments are USB devices.

@subsection driver_win Windows USB Driver Installation
On Windows, the supplied USB driver with this SDK must be installed. 
See the seperate manual.

@subsection driver_mac Apple Mac OS X Driver
No drivers are required on Mac OS X.

*/

/** \file i1Pro.h
* \brief Main include file for the i1Pro SDK
*/

#ifndef I1PRO_H
#define I1PRO_H

#include "MeasurementConditions.h"

#if defined( _MSC_VER ) && _MSC_VER < 1600
    typedef signed   __int32 I1_Integer;
    typedef unsigned __int32 I1_UInteger;
#else
  #include <stdint.h>
  typedef int32_t  I1_Integer;
  typedef uint32_t I1_UInteger;
#endif


#ifdef __cplusplus
  extern "C" {
#endif


/******************************************************************************/
/******************************************************************************/
/**
  @defgroup resultType Result Type
  @{
*/

/** @brief Most functions in the i1Pro SDK will return values from this enumeration to
    indicate the return status of function calls.
    They return eNoError on success, or one of the values on failure.
    Use I1_GetOption(I1_LAST_ERROR_TEXT) for more details about the error.
*/
enum {
  eNoError                      =  0,     /**< no error, success */

  /* wrong usage of functions, wrong mode, parameters, ... Fix the program flow in your app */
  eException                    =  1,     /**< internal exception */
  eBadBuffer                    =  2,     /**< size of the buffer is not large enough for the data */
  eInvalidHandle                =  9,     /**< I1_DeviceHandle is no longer valid, no device associated to this handle (device unplugged) */
  eInvalidArgument              = 10,     /**< a passed method argument is invalid (e.g. NULL) */
  eDeviceNotOpen                = 11,     /**< the device is not open. Open device first */
  eDeviceNotConnected           = 12,     /**< the device is not physically attached to the computer */
  eDeviceNotCalibrated          = 13,     /**< the device has not been calibrated or the calibration has expired */
  eNoDataAvailable              = 14,     /**< measurement not triggered, index out of range (in scan mode) */
  eNoMeasureModeSet             = 15,     /**< no measure mode has been set */
  eNoReferenceChartLine         = 17,     /**< no reference chart line for correlation set */
  eNoSubstrateWhite             = 18,     /**< no substrate white reference set */
  eNotLicensed                  = 19,     /**< function not licensed (available) for this device */
  eDeviceAlreadyOpen            = 20,     /**< the device has been opened already */

  /* user device handling error. Instruct user what to do */
  eDeviceAlreadyInUse           = 51,     /**< the device is already in use by another application */
  eDeviceCommunicationError     = 52,     /**< a USB communication error occurred, try to disconnect and reconnect the device */
  eUSBPowerProblem              = 53,     /**< a USB power problem was detected. If you run the instrument on a self-powered USB hub, check the hub's power supply. If you run the instrument on a bus-powered USB hub, reduce the number of devices on the hub or switch to a self-powered USB hub */
  eNotOnWhiteTile               = 54,     /**< calibration failed because the device might not be on its white tile or the protective white tile slider is closed */

  eStripRecognitionFailed       = 60,     /**< recognition is enabled and failed. Scan again */
  eChartCorrelationFailed       = 61,     /**< could not map scanned data to the reference chart. Scan again */
  eInsufficientMovement         = 62,     /**< distance of movement too short on the i1Pro2 ruler during scan. The device didn't move. Scan again */
  eExcessiveMovement            = 63,     /**< distance of movement exceeds licensed i1Pro2 ruler length. Print shorter patch lines */
  eEarlyScanStart               = 64,     /**< missed patches at the beginning of a scan. The user must wait at least 500 milliseconds between pressing the button and starting to move the device */
  eUserTimeout                  = 65,     /**< the user action took too long, try again quicker */
  eIncompleteScan               = 66,     /**< the user did not scan over all patches */
  eDeviceNotMoved               = 67,     /**< the user did not move during scan measurement (no Zebra Ruler data received). May be the user lifted the device */

  /* device may be corrupt. Tell user she/he should contact customer support */
  eDeviceCorrupt                = 71,     /**< an internal diagnostic detected a problem with the instruments data. Please check using i1Diagnostics to obtain more information */
  eWavelengthShift              = 72      /**< an internal diagnostic of wavelength shift detected a problem with spectral sensor. Please check with i1Diagnostics to obtain more information */
};
typedef I1_UInteger I1_ResultType;

/*@} end resultType*/


/******************************************************************************/
/******************************************************************************/
/**
  @defgroup keys Key and Value Definitions
  @{
  Keys and values for all of the I1_GetXXXOption and I1_SetXXXOption APIs. 
  All options are read/write unless otherwise specified.
  @note All keys and values in MeasurementConditions.h are individual options 
  for each device.
*/
#define I1_VALUE_DELIMITER                  ";"                           /**< the delimiter used to separate multiple values in a string */

#define I1_YES                              "1"                           /**< value - for various options (global and device specific options) */
#define I1_NO                               "0"                           /**< value - for various options (global and device specific options) */

/** @warning On Windows it is mandatory to call the reset command 'I1_SetGlobalOption(I1_RESET, I1_ALL)' to close the library before application
    exits or the library is unloaded. This is voluntary on other platforms.\n Use I1_SetOption(dev, I1_RESET, I1_MEASUREMENT_MODE) to set the current
    measure mode to its initial condition */
#define I1_RESET                            "Reset"                       /**< key - reset command. Will release internal objects. Write-only */
#define I1_ALL                              "All"                         /**< value - resets the SDK to its initial state. Closes all devices, removes registered callbacks. This is nearly equivalent to unloading and reloading the SDK. Read-only */

/**
  @defgroup global_keys Global Keys and Values
  @{
  @brief Key and value definitions specific to I1_GetGlobalOption and I1_SetGlobalOption. The values of global keys 
  affect all devices.
*/
#define I1_SDK_VERSION                      "SDKVersion"                  /**< key - the version of sdk in form of 'Major.Minor.Revision.Build Suffix' where ' Suffix' may be empty. Read-only */
#define I1_SDK_VERSION_MAJOR                "SDKVersionMajor"             /**< key - the major number as string. Read-only */
#define I1_SDK_VERSION_MINOR                "SDKVersionMinor"             /**< key - the minor number as string. Read-only */
#define I1_SDK_VERSION_REVISION             "SDKVersionRevision"          /**< key - the revision number as string. Read-only */
#define I1_SDK_VERSION_BUILD                "SDKVersionBuild"             /**< key - the build number as string. Read-only */
#define I1_SDK_VERSION_SUFFIX               "SDKVersionSuffix"            /**< key - the suffix as a string. Final versions have an empty suffix. Read-only */

#define I1_LAST_ERROR                       "LastError"                   /**< key - the last error result, which is an I1_ResultType expressed as a string. Read-only */
#define I1_LAST_ERROR_TEXT                  "LastErrorText"               /**< key - a short error description of the last error result. This text is not localized and should not be displayed to the user. Instead, provide this string to the SDK support. Read-only */
#define I1_LAST_ERROR_NUMBER                "LastErrorNumber"             /**< key - an SDK internal error code for last error. This text should not be displayed to the user. Instead, provide this string to the SDK support. Read-only */

#define I1_ON_MEASUREMENT_SUCCESS_NO_LED_INDICATION  "OnMeasurementSuccessNoLedIndication" /**< key - set this value to I1_YES if the application has control over the user indicator LED on i1Pro RevE devices after a successful measurement. If the measurement fails, the indicator LEDs are switched to their fail state automatically. After the first scan in dual scan mode, the indicator LEDs must be updated to show the correct direction for the backward scan. See #I1_INDICATOR_LED_KEY for more information.\n
                                                                               This key can be used for a device or globally. Using the key for one device with I1_SetOption(), will change the behavior of that device only, while using it globally with I1_SetGlobalOption(), it will change the default behavior when opening a device.\n Possible values: I1_YES, I1_NO. Default: I1_NO */
/*@} end global_keys*/



/**
  @defgroup device_keys Device Keys and Values
  @{
  @brief Device key and value definitions for I1_GetOption and I1_SetOption. 
  These options are reset to their default values when you use the device for 
  the first time in the SDK session, or if the user disconnects and reconnects 
  the device, or a reset on the device is called.
*/
#define I1_SERIAL_NUMBER                    "SerialNumber"                /**< key - the serial number of the device. Read-only */
#define I1_PRECISION_CALIBRATION_KEY        "PrecisionCalibration"        /**< key - Enable precision calibration. We suggest to enable this. See I1_Calibrate(). Possible values: I1_YES, I1_NO. Default: I1_NO */
#define I1_SIMULATE_LAMP_RESTORE_KEY        "SimulateLampRestore"         /**< key - if set to I1_YES, each I1_Calibrate() will simulate the lamp restore process to test your #eI1ProLampRestore handling. See I1_Calibrate(). For debugging only, dont use this in release applications! Possible values: I1_YES, I1_NO. Default: I1_NO */
#define I1_DEVICE_PATH_KEY                  "DevicePath"                  /**< key - the USB path to the device used to identify the device in the system USB tree. This key can be used with I1_GetOption and a valid device handle. The device must not be opened. Read-only */

/**
  @defgroup measurement_mode_kv Measurement Modes
  @{
*/
#define I1_AVAILABLE_MEASUREMENT_MODES      "AvailableMeasurementModes"   /**< key - all available measurement modes. Separated by #I1_VALUE_DELIMITER. Read-only */
#define I1_MEASUREMENT_MODE                 "MeasurementMode"             /**< key - the active measurement mode. Changing the measurement mode after a measurment will flush the cached results. */
#define I1_MEASUREMENT_MODE_UNDEFINED       "MeasurementModeUndefined"    /**< value - the default for #I1_MEASUREMENT_MODE */
#define I1_REFLECTANCE_SPOT                 "ReflectanceSpot"             /**< value - measurement mode for one spot measurement on a reflective surface */
#define I1_REFLECTANCE_SCAN                 "ReflectanceScan"             /**< value - measurement mode for a scan on a reflective surface (chart) */
#define I1_EMISSION_SPOT                    "EmissionSpot"                /**< value - measurement mode for an emission measurement on an emitting probe (display) */
#define I1_AMBIENT_LIGHT_SPOT               "AmbientLightSpot"            /**< value - measurement mode for an ambient light measurement */
#define I1_AMBIENT_LIGHT_SCAN               "AmbientLightScan"            /**< value - measurement mode for an ambient light scan (flash) */
#define I1_DUAL_REFLECTANCE_SPOT            "DualReflectanceSpot"         /**< value - measurement mode for a spot measurement with Tungsten filament lamp and UV Led. Only available for i1Pro RevE devices */
#define I1_DUAL_REFLECTANCE_SCAN            "DualReflectanceScan"         /**< value - measurement mode for a two way scan measurement with Tungsten filament lamp and UV Led. Only available for i1Pro RevE devices. Must be performed with i1Pro RevE ruler. */
/*@} end measurement_mode_kv*/

/**
  @defgroup devcap_keys Device Capability Keys
  @{
*/
#define I1_HAS_UV_LED_KEY                   "HasUVLed"                    /**< key - the device has a UV LED. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_UVCUT_FILTER_KEY             "HasUVcutFilter"              /**< key - the device has a physical UV cut filter. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_WAVELENGTH_LED_KEY           "HasWavelengthLed"            /**< key - the device has a wavelength LED. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_ZEBRA_RULER_SENSOR_KEY       "HasZebraRulerSensor"         /**< key - the device has a Zebra Ruler Sensor. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_INDICATOR_LED_KEY            "HasIndicatorLed"             /**< key - the device has indicator LEDs. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_AMBIENT_LIGHT_KEY            "HasAmbientLight"             /**< key - the device has the ambient light feature. Read-only. Possible values: I1_YES, I1_NO */
#define I1_HAS_LOW_RESOLUTION_KEY           "HasLowResolution"            /**< key - the device has the low resolution feature. Read-only. Possible values: I1_YES, I1_NO */
#define I1_MAX_RULER_LENGTH_KEY             "MaxRulerLength"              /**< key - maximal ruler length in millimeters. Read-only. Possible values: an integer expressed as a string */
#define I1_IS_EMISSION_ONLY_KEY             "IsEmssionOnly"               /**< key - can the i1Monitor device measure emission only? Read-only. Possible values: I1_YES, I1_NO */
#define I1_HW_REVISION_KEY                  "HWRevision"                  /**< key - the revision of the hardware device. Read-only. Possible values: A,B,C,D,E,... */
#define I1_SUPPLIER_NAME_KEY                "SupplierName"                /**< key - the name of the branded supplier. Read-only */

#define I1_DEVICE_TYPE_KEY                  "DeviceTypeKey"               /**< key - the family name of the device. Read-only */
#define I1_DEVICE_TYPE_I1PRO                "i1Pro"                       /**< value - the i1Pro device family */
/*@} end devcap_keys*/


/**
  @defgroup measurement_device_keys Device Behaviors
  @{
  @brief These options are available only after you set the measurement mode. 
  They will be reset if the user disconnects and reconnects the device or a 
  reset is called on the device.
*/

/**
  @defgroup patch_recog Patch Recognition
  @{
*/
#define I1_AVAILABLE_PATCH_RECOGNITIONS_KEY "AvailableRecognitionsKey"    /**< key - the list of available patch recognition modes. Separated by #I1_VALUE_DELIMITER. Read-only */
#define I1_PATCH_RECOGNITION_KEY            "RecognitionKey"              /**< key - the mode of patch recognition when in scan mode. See 'ChartDesignRules.pdf' */
#define I1_PATCH_RECOGNITION_DISABLED       "RecognitionDisabled"         /**< value - the default for #I1_PATCH_RECOGNITION_KEY, which is no patch recognition */
#define I1_PATCH_RECOGNITION_BASIC          "RecognitionBasic"            /**< value - algorithm for scans without an i1Pro RevE ruler */
#define I1_PATCH_RECOGNITION_CORRELATION    "RecognitionCorrelation"      /**< value - algorithm for scans without an i1Pro RefE ruler. Correlates patches and references. See #I1_SetReferenceChartLine for more details */
#define I1_PATCH_RECOGNITION_POSITION       "RecognitionPosition"         /**< value - algorithm for scans with an i1Pro RevE ruler. Requires a valid #I1_NUMBER_OF_PATCHES_PER_LINE value, which must be at least 6. */
#define I1_PATCH_RECOGNITION_FLASH          "RecognitionFlash"            /**< value - algorithm for scans in ambient light mode for flash detection */
#define I1_PATCH_RECOGNITION_RECOGNIZED_PATCHES "RecognitionRecognizedPatches" /**< value - number of recognized patches before correlation algorithm is applied. Available in #I1_PATCH_RECOGNITION_CORRELATION only. See # I1_TriggerMeasurement for more details */
/*@} end patch_recog*/

/**
  @defgroup ref_chart Reference Charts
  @{
*/
#define I1_REFERENCE_CHART_COLOR_SPACE_KEY  "ReferenceChartColorSpaceKey" /**< key - color space for #I1_SetReferenceChartLine. Only enabled with #I1_PATCH_RECOGNITION_CORRELATION */
#define I1_REFERENCE_CHART_RGB              "ReferenceChartRGB"           /**< value - RGB values */
#define I1_REFERENCE_CHART_CMYK             "ReferenceChartCMYK"          /**< value - CMYK values */
#define I1_REFERENCE_CHART_LAB              "ReferenceChartLab"           /**< value - Lab values */
/*@} end ref_chart*/

#define I1_LOW_RESOLUTION_KEY               "LowResolution"               /**< key - improved patch recognition algorithm for low resolution. Only available in Basic/Correlation recognition. Feature must be licensed on device (I1_HAS_LOW_RESOLUTION_KEY). Possible values: I1_YES, I1_NO \n
                                                                          Low resolution test chart: For output that is viewed at a larger distance, including many applications in solvent printing, it is common to use low resolution in order to achieve high ink coverage at high speed. When measuring a test chart with poor edge definition due to low output resolution, enable this setting to help your i1Pro recognize your test chart patches properly. */

#define I1_ADAPTIVE_MEASUREMENT_KEY         "AdaptiveMeasurement"         /**< key - makes a trial measurement first to get the best measurement result. Disabling it lowers the measurement duration and result quality. Available in Emission and AmbientSpot mode. Possible values: I1_YES, I1_NO. Default: I1_YES */
#define I1_TIME_SINCE_LAST_CALIBRATION      "TimeSinceLastCalibration"    /**< key - time in seconds since the last calibration. -1 if not calibrated. Read-only */
#define I1_TIME_UNTIL_CALIBRATION_EXPIRE    "TimeUntilCalibrationExpire"  /**< key - time in seconds until the calibration expires. -1 if not calibrated or expired. Read-only */
#define I1_MEASURE_COUNT                    "MeasureCount"                /**< key - the number of measurements since the last calibration. Read-only */
#define I1_LAST_AUTO_DENSITY_FILTER         "LastAutoDensityFilter"       /**< key - the actual density filter name of the last measurement. Read-only */

/**
  @defgroup scan_dir Scan Direction
  @{
*/
#define I1_SCAN_DIRECTION_KEY               "ScanDirectionKey"            /**< key - the direction of the next dual scan with the i1Pro RevE ruler. Set to forward or backward before starting a dual scan */
#define I1_SCAN_DIRECTION_FORWARD           "1"                           /**< value - M0 scan. First scan with Tungsten filament lamp */
#define I1_SCAN_DIRECTION_BACKWARD          "2"                           /**< value - UV scan. Second scan with UV Led */
#define I1_SCAN_DIRECTION_UNDEFINED         "0"                           /**< value - undefined scan direction. Not valid for a scan; change it to forward or backward */
#define I1_NUMBER_OF_PATCHES_PER_LINE       "PatchesPerLine"              /**< key - the number of patches per line with #I1_PATCH_RECOGNITION_POSITION. Required */

#define I1_LAST_SCAN_DIRECTION_KEY          "LastScanDirectionKey"        /**< key - the direction information from the i1Pro RevE ruler after a successful scan. The value can be used to manually turn on the correct indicator LED after a forward scan (#I1_INDICATOR_LED_WAIT_FOR_SCAN_LEFT, #I1_INDICATOR_LED_WAIT_FOR_SCAN_RIGHT). Only available with active #I1_PATCH_RECOGNITION_POSITION. Read-only */
#define I1_LAST_SCAN_RIGHT_TO_LEFT          "-1"                          /**< value - user scanned from right to left */
#define I1_LAST_SCAN_LEFT_TO_RIGHT          "1"                           /**< value - user scanned from left to right */
#define I1_LAST_SCAN_UNDEFINED              "0"                           /**< value - no direction information */
/*@} end scan_dir*/

/**
  @defgroup ind_led Indicator LED
  @{
*/
#define I1_INDICATOR_LED_KEY                   "IndicatorLedKey"          /**< key - controls the user indicator LED on i1Pro RevE devices after a measurement. See #I1_ON_MEASUREMENT_SUCCESS_NO_LED_INDICATION. Write-only */
#define I1_INDICATOR_LED_MEASUREMENT_SUCCEEDED "IndicatorLedSucceeded"    /**< value - signal a successful measurement to the user with a green LED sequence */
#define I1_INDICATOR_LED_MEASUREMENT_FAILED    "IndicatorLedFailed"       /**< value - signal a failure measurement to the user with a red LED sequence */
#define I1_INDICATOR_LED_MEASUREMENT_WRONG_ROW "IndicatorLedWrongRow"     /**< value - signal a measured wrong row to the user with 1 green and 2 red LED sequence */
#define I1_INDICATOR_LED_WAIT_FOR_SCAN_LEFT    "IndicatorLedWait4LeftScan"  /**< value - signal a user to scan in the left direction with a blue LED sequence */
#define I1_INDICATOR_LED_WAIT_FOR_SCAN_RIGHT   "IndicatorLedWait4RightScan" /**< value - signal a user to scan in the right direction with a blue LED sequence */
#define I1_INDICATOR_LED_WAIT_FOR_SCAN         "IndicatorLedWait4Scan"    /**< value - signal a user to scan in an unknown direction with a blue LED sequence */
#define I1_INDICATOR_LED_OFF                   "IndicatorLedOff"          /**< value - keep the indicator LED off. Useful in a sequence of emissive measurements */
#define I1_INDICATOR_LED_I1IO_POSITION_ACCEPT  "IndicatorLedIOPositionAccept" /**< value - signal user that position has been accpeted during chart positioning with i1iO */
/*@} end ind_led*/

/**
  @defgroup illum Illuminants
  @{
*/
#define I1_AVAILABLE_ILLUMINATIONS_KEY      "AvailableIlluminationsKey"   /**< key - all available illuminations this device is capable of. Separated by #I1_VALUE_DELIMITER. Read-only */
#define I1_AVAILABLE_RESULT_INDEXES_KEY     "AvailableResultIndexesKey"   /**< key - all available result filters for the current measurement mode. Separated by #I1_VALUE_DELIMITER. Read-only */
#define I1_RESULT_INDEX_KEY                 "ResultIndexKey"              /**< key - defines which result (I1_GetSpectrum/Tristimulus/Density) you get. Specific to each measure mode. You can check availability with #I1_AVAILABLE_RESULT_INDEXES_KEY. M0/M1/M2 are available for a dual measurement. While on a UV Cut device, only M2 is available. Default: M0, on UV Cut devices: M2 or Emissive on emissive modes */
#define I1_ILLUMINATION_CONDITION_M0        "M0"                          /**< value - ISO 13655, CIE Illuminant A, UV included, aka 'No Filter'. Tungsten lamp with a CCT of ~2856K. UV content is not specifically controlled. */
#define I1_ILLUMINATION_CONDITION_M1        "M1"                          /**< value - ISO 13655, CIE Illuminant D50. UV included, content must match the one of D50, thereby minimizing variations in the measurements due to fluorescence from optical brighteners. */
#define I1_ILLUMINATION_CONDITION_M2        "M2"                          /**< value - ISO 13655, UV excluded, aka UV Cut. The spectrum of the illuminant is not exactly specified, the illuminant does not contain any UV energy (may be natural property of the illuminant, or a UV Cut filter may be used), (e.g., Tungsten Lamp with UV Cut filter). Minimizes variations in the measurements due to fluorescence from optical brighteners, but results do not match the visual impression. */
#define I1_EMISSIVE                         "Emissive"                    /**< value - an emissive (including ambient) result */
/*@} end illum*/

#define I1_MEASUREMENT_GEOMETRY_KEY         "MeasurementGeometryKey"      /**< key - the physical measurement geometry of the device. Read-only */
#define I1_MEASUREMENT_GEOMETRY_45_0        "45:0"                        /**< value - annular illumination by a ring reflector at 45 degrees and measured with 0 degrees */

/*@} end measurement_device_keys*/

/*@} end device_keys*/

/*@} end keys*/


/******************************************************************************/
/******************************************************************************/
/**
  @ingroup device
  @brief An opaque datatype representing a handle to an i1 device.

  A handle of this type can be obtained by calling #I1_GetDevices.

  This device handle is used to perform operations on a specific device instance. 
  When finished with the device handle, you should call #I1_CloseDevice.
*/
typedef struct I1_Device_ *I1_DeviceHandle;



/******************************************************************************/
/******************************************************************************/

#if !defined(I1_API)
  #if defined(_WIN32) || defined(__CYGWIN__)
    #define I1_API extern __declspec(dllimport)
  #else
    #define I1_API
  #endif
#endif

/* Declare the calling convention for callbacks */
#if !defined(I1_CALLING_CONVENTION)
  #if defined(_MSC_VER)
    #if defined(_M_IX86)
      #define I1_CALLING_CONVENTION __cdecl
    #else
      #define I1_CALLING_CONVENTION
    #endif
  #elif defined(__GNUC__)
    #if defined(__i386__)
      #define I1_CALLING_CONVENTION __attribute__((cdecl))
    #else
      #define I1_CALLING_CONVENTION
    #endif
  #else
    #error You need to define the cdecl calling convention
  #endif
#endif



/******************************************************************************/
/**
  @defgroup device Device Handling
  @brief These functions deal with connected devices and device handles.
  @{
*/


/** @brief Get a pointer to an array of device handles for devices currently 
    connected to the computer.
    @param[out] devices a pointer to an internal static array of device handles
    @param[out] count number of entries in the array
    @return eNoError on success

    Each handle represents a connected device. A handle becomes invalid if the 
    device is closed or disconnected. Each subsequent call of I1_GetDevices will
    invalidate the array returned by the previous call. The last entry in the 
    array is a NULL pointer. The memory used by the array is maintained by the 
    library, so do not attempt to free this memory. The number of entries in the
    array is returned in count.
    \n\n
    The handles returned in this array are not valid to use in most APIS until 
    opened by a call to #I1_OpenDevice. You do not need to call
    #I1_CloseDevice on the handles returned in the array unless you
    have explicitly opened them via I1_OpenDevice.
*/
I1_API
I1_ResultType I1_GetDevices(I1_DeviceHandle **devices, I1_UInteger *count);


/** @brief Opens a handle to a device.
    @param[in] devHndl handle to the device to be opened
    @return eNoError on success

    This function opens a device via a handle received from #I1_GetDevices.
    It is required to open a device handle before you can call any other function on it.
    \n\n
    Once you have finished using the device, you can close it with a call to 
    #I1_CloseDevice.
*/
I1_API
I1_ResultType I1_OpenDevice(I1_DeviceHandle devHndl);


/** @brief Closes the device associated with the handle.
    @param[in] devHndl handle to the device
    @return eNoError on success

    You should only call I1_CloseDevice on a handle that has previously been 
    opened by a call to #I1_OpenDevice.
    \n\n
    All internal buffers associated with the object are flushed and freed, and 
    the USB connection is closed, even if the call fails. Upon return, the 
    handle referenced by devHndl is no longer valid. Attempting to use it will 
    result in undefined behavior.
    \n\n
    All devices are closed as well when the library is unloaded (e.g. at application exit).
*/
I1_API
I1_ResultType I1_CloseDevice(I1_DeviceHandle devHndl);


/*@} end device*/


/******************************************************************************/
/** @defgroup conditions Get/Set Device Options
    @{
*/

/** @brief Set a global option for all devices
    @param[in] key a null terminated string. Must not be empty or null
    @param[in] value a null terminated string. Must not be empty or null
    @return eNoError on success
*/
I1_API
I1_ResultType I1_SetGlobalOption(const char *key, const char *value);


/** @brief Get a global option, writing the string to the user provided buffer
    @param[in] key a null terminated string. Must not be empty or null
    @param[out] buffer memory location of where to store the result. May be null to query the size
    @param[in,out] size on entry: a pointer to the size of the buffer.\n
                        on exit: if buffer is null, a pointer to the size required to fit the option string, including the null terminator.\n
                        Must not be null
    @return eNoError on success

    If buffer is big enough, writes the result into buffer. If the provided 
    buffer size is smaller than the result, the buffer is not modified and 
    eBadBuffer is returned. To query the buffer size, pass a null buffer. It is 
    not guranteed that identic function calls need/return the same buffer size. 
    A good default buffer size is 256 bytes. Keys which may require a larger 
    buffer are marked. The buffer must be big enough to hold the trailing nul 
    character.
*/
I1_API
I1_ResultType I1_GetGlobalOption(const char *key, char *buffer, I1_UInteger *size);


/**
    @brief Get a global option as a string, for debugging purposes only
    @param[in] key a null terminated string. Must not be empty or null
    @return A constant string pointer to an internal static string containing the desired information

    The return value is a pointer to an internal static string. The data will 
    be overwritten by the next I1_GetGlobalOptionD call. An empty string is 
    returned if the key was not recognized.

    @warning This function is for debugging purposes only. Because you don't 
    have to provide a buffer, you can use the return value in e.g. printf(). 
    It is not multithread safe. You should use #I1_GetGlobalOption instead.
*/
I1_API
const char* I1_GetGlobalOptionD(const char *key);


/** @brief Set a device-specific option
    @param[in] devHndl handle to the device. Must not be null
    @param[in] key a null terminated string. Must not be empty or null
    @param[in] value a null terminated string. Must not be empty or null
    @return eNoError on success
*/
I1_API
I1_ResultType I1_SetOption(I1_DeviceHandle devHndl, const char *key, const char *value);


/** @brief Get a device-specific option, writing the string to a user provided buffer
    @param[in] devHndl handle to the device. Must not be null
    @param[in] key a null terminated string. Must not be empty or null
    @param[out] buffer to hold the result. May be null to query the size
    @param[in,out] size on entry: a pointer to the size of the buffer pointed to by buffer.\n
                        on exit: if buffer is null, a pointer to the size of the option string including the null terminator.\n
                        Must not be null
    @return eNoError on success

    If the buffer is large enough, this call writes the results into buffer. If 
    the provided buffer size is smaller than the result, the buffer is not 
    modified and #eBadBuffer is returned. To query the buffer
    size, pass a null buffer. There is an inherent race condition implied, so 
    it is not guaranteed that same function call needs a buffer of the same 
    size. A good default buffer size is 256 bytes. Keys which may require a 
    bigger buffer are documented. The buffer must be big enough to hold the 
    trailing null character.
*/
I1_API
I1_ResultType I1_GetOption(I1_DeviceHandle devHndl, const char *key, char *buffer, I1_UInteger *size);


/** @brief Get a device-specific option as a string, for debugging purposes only
    @param[in] devHndl handle to the device. Must not be null
    @param[in] key a null terminated string. Must not be empty or null
    @return A constant pointer to an internal static string containing the desired information.

    The return value is a pointer to an internal static string. The data will 
    be overwritten by the next I1_GetOption call. An empty string is returned 
    if the key was not recognized.

    @warning This function is for debugging purposes only. Because you don't 
    have to provide a buffer, you can use the return value in e.g. printf(). It 
    is not multithread safe. You should use #I1_GetOption instead.
*/
I1_API
const char* I1_GetOptionD(I1_DeviceHandle devHndl, const char *key);


/*@} end conditions*/


/******************************************************************************/
/** @defgroup status Connection & Button Status
    @{
*/

/** @brief result from I1_GetConnectionStatus() is hex encoded
     - Bit 0: i1Pro connected
     - Bit 1: i1Pro open
*/
enum {
  eInvalidConnectionHandle      = 0x00,   /**< I1_DeviceHandle is no longer valid, no device associated to this handle (device unplugged) */
  eI1ProClosed                  = 0x01,   /**< i1Pro is plugged in, communication to device not established */
  eI1ProOpen                    = 0x03    /**< i1Pro is open and ready to use, communication to device established */
};
typedef I1_UInteger I1_ConnectionStatusType;


/** @brief Test status of device handle. The handle must not be opened before.
    eInvalidConnectionHandle is returned if the device is no longer connected to the computer.
    This function will not change the status of any associated device.
    @param[in] devHndl handle to the device. Must not be null
    @return eInvalidConnectionHandle, eI1ProClosed, eI1ProOpen
*/
I1_API
I1_ConnectionStatusType I1_GetConnectionStatus(I1_DeviceHandle devHndl);



/** @brief button some of the values returned by I1_GetButtonPressedD()
*/
enum {
  eButtonIsPressed              = 1000,   /**< i1Pro button is pressed */
  eButtonNotPressed             = 1001    /**< i1Pro button is not pressed */
};
typedef I1_UInteger I1_ButtonStatusType;


/** @brief Test if the button on the i1Pro device has been pressed by the user
    @param[in] devHndl handle to the device. Must not be null
    @return eButtonIsPressed if button was pressed since last time I1_GetButtonStatusD was called.
    Or eButtonNotPressed if button was not pressed.
    Or any other value from I1_ResultType like eInvalidHandle, eDeviceNotOpen

    The state will be set to #eButtonIsPressed if the user
    presses the i1Pro button.
    The state will be set to #eButtonNotPressed after calling
    #I1_GetButtonStatusD.
    You can use this method to wait for the user before scanning.

    @code
    printf("Press the i1Pro button");
    while(I1_GetButtonStatusD(devHandl) != eButtonNotPressed) {
      sleep(1);
    }
    I1_TriggerMeasurement(devHandl);
    @endcode

    @warning Polling is a bad solution, especially in user interface threads.
    Use #I1_RegisterDeviceEventHandler to get informed about
    events in a non-polling manner. The I1_GetButtonStatusD function should be
    used for development or debugging purposes only.
*/
I1_API
I1_ButtonStatusType I1_GetButtonStatusD(I1_DeviceHandle devHndl);

/*@} end status*/


/******************************************************************************/
/** @defgroup cal_meas Calibrate & Trigger Measurement
    @brief Each measurement mode must be calibrated before a measurement can be
    triggered.
    @{
*/

/** @brief Calibrates the i1 hardware device in the current measurement mode
    @param[in] devHndl handle to the device. Must not be null
    @return eNoError on success or eNotOnWhiteTile if device was not placed on 
    its white tile (or white tile slider is closed).

    Before any calibration is done, you should select your desired measurement 
    mode via #I1_SetOption (I1_MEASUREMENT_MODE, mode). A calibration is only 
    applied to the current measurement mode. After switching to another mode, 
    the previous calibration will be saved and restored after  switching back.
    If the wavelength LED is licensed, reflectance spot mode is calibrated 
    automatically in the background for non-reflectance spot modes.
    \n\n
    Calibration will be lost after a reset, disconnect or after library is 
    unloaded. If a calibration fails in one mode, all other modes of the device 
    will get uncalibrated. Keep in mind that a calibration is not sustainable 
    for too long due to temperature changes and other factors. You can get the 
    maximum time in seconds until the calibration expires with
    #I1_TIME_UNTIL_CALIBRATION_EXPIRE (assuming perfect conditions).
    #I1_TIME_SINCE_LAST_CALIBRATION returns the time in seconds
    since the last calibration. An uncalibrated measure mode returns "-1" for 
    both keys. A calibration is valid for a maximum of about four hours except 
    when in Ambient-mode where it is valid for 31 days. Every calibration 
    requires that the sensor is placed on its own white tile with the 
    protective slider open. To check which measurement modes are available for 
    this device, use the #I1_AVAILABLE_MEASUREMENT_MODES option.

    @note If #I1_PRECISION_CALIBRATION_KEY is set to yes, calibrating
    reflectance modes will also check the built in Tungsten filament lamp.
    If a lamp drift is detected, the lamp will be restored automatically. 
    Restoring the standard lamp condition adds time to the
    calibration process (about 2 minutes). In that case, an event
    #eI1ProLampRestore is emitted. Your event handler should inform the user
    that calibration takes longer than usual. Suggested message:
    @verbatim Restoring standard lamp conditions. This is infrequently 
    necessary. Please leave the instrument on the Calibration Plate during 
    the process.@endverbatim
    Note that restoring the lamp is only needed in rare occasions.
    To test your event handling, you can enable #I1_SIMULATE_LAMP_RESTORE_KEY
    (I1_PRECISION_CALIBRATION_KEY must be enabled as well).
*/
I1_API
I1_ResultType I1_Calibrate(I1_DeviceHandle devHndl);


/** @brief Triggers a measurement depending on the current measurement mode
    @param[in] devHndl handle to the device. Must not be null
    @return may return #eDeviceNotCalibrated if a (re)calibration is necessary. 
    If eUserTimeout is returned in #I1_DUAL_REFLECTANCE_SCAN, the scan took too 
    long (> 20 seconds) or the backward scan has not been started within a 
    specific time period.

    Before a measurement can be triggered, the device must be calibrated in the 
    desired measurement mode. In #I1_REFLECTANCE_SCAN mode, a
    patch recognition or correlation can be activated (see 
    #I1_PATCH_RECOGNITION_KEY). Use #I1_GetSpectrum, #I1_GetTriStimulus or 
    #I1_GetDensity to fetch the results.

    If you enabled the correlation algorithm in the reflectance scan mode and 
    you receive an #eChartCorrelationFailed error, you can check
    if the user moved the device too fast over the strip by getting the property 
    #I1_PATCH_RECOGNITION_RECOGNIZED_PATCHES. This will return the
    number of patches recognized during the scan, and if it is less than the 
    number of expected patches it usually indicates the scan should be repeated 
    with a lower speed.
    \n\n
    In #I1_DUAL_REFLECTANCE_SCAN mode, a forward and a backward
    scan must be performed. Set the appropriate #I1_SCAN_DIRECTION_KEY
    property before you trigger the measurement. In the forward scan,
    M0 (NoFilter) measurements are taken and the position of the patches are 
    determined. After a successful forward scan, the device continues sending 
    position data. Set the backward direction and start taking the UV 
    measurements. The position data are used to extract the UV measurements from 
    the middle of the patch. The M1 and M2 results are calculated with M0 and UV 
    measurements. After a backward scan, the device stops sending position data. 
    If you already triggered a forward scan, but don't want to execute the 
    backward scan, the position data transfer can be aborted by setting the scan 
    direction to #I1_SCAN_DIRECTION_FORWARD.
    The i1Pro RevE Zebra ruler is required for this mode. And the device must have 
    sensors integrated (#I1_HAS_ZEBRA_RULER_SENSOR_KEY).
*/
I1_API
I1_ResultType I1_TriggerMeasurement(I1_DeviceHandle devHndl);


/*@} end cal_meas*/


/******************************************************************************/
/** @defgroup results Measurement Results
    @brief Retrieve measurement results from a previously triggered measurement.

    XRGA (X-Rite Graphic Arts Standard): i1Pro RevE devices are factory 
    calibrated to the XRGA calibration standard for reflectance measurements. 
    Previous revisions of hardware will automatically be translated to XRGA 
    using this SDK.
    \n\n
    To fetch the result of a previously triggered spot measurement, use 0
    as the Index.
    \n\n
    To fetch the result of a previously triggered scan, specify an index 
    between 0 and (I1_GetNumberOfAvailableSamples() - 1). If no measurement has 
    been triggered or if the specified index is out of range, eNoDataAvailable 
    is returned.

    @see <a href="http://www.xrite.com/xrite-graphic-arts-standard">X-Rite Graphic Arts Standard</a>
    @{
*/

/** @brief Returns the number of available samples for the current measurement 
    mode and result index
    @param[in] devHndl handle to the device. Must not be null
    @return number of cached samples available in #I1_GetSpectrum,
    #I1_GetTriStimulus or #I1_GetDensity.
    - 0 if no measurement has been triggered
    - 1 if the measurement is set to spot
    - number of scanned samples in scan mode
    - -1 on failure

    In dual scan mode, make sure you have the correct #I1_RESULT_INDEX_KEY
    activated: M0, M1 or M2.
*/
I1_API
I1_Integer I1_GetNumberOfAvailableSamples(I1_DeviceHandle devHndl);


/** @brief Get the spectrum of a previously triggered measurement
    @param[in]  devHndl handle to the device
    @param[out] spectrum pointer to the resulting array. Must be large enough 
                to hold 36 floating-point values, and cannot be null
    @param[in]  index zero-based index of the spectra. For spot measurement 
                results use zero @return eNoError on success
*/
I1_API
I1_ResultType I1_GetSpectrum(I1_DeviceHandle devHndl, float spectrum[SPECTRUM_SIZE], I1_Integer index);


/** @brief Get the color vector of a previous triggered measurement
    @param[in]  devHndl handle to the device
    @param[out] tristimulus pointer to the resulting array. Must be large enough 
                to hold 3 floating-point values, and cannot be null
    @param[in]  index zero-based index of the tristimuli. For spot measurement 
                results use zero
    @return eNoError on success

    The color space COLOR_SPACE_RGB must be used with caution. Normally a 
    monitor profile is used to convert color information from a device 
    independent space (e.g. XYZ) to RGB. The profile is only valid and useful 
    for the (calibrated) monitor which it was created with. TFT and CRT monitors 
    differ substantially. What we use for our RGB calculation is a generic 
    profile for a standard CRT monitor. This means that it will never return 
    perfect RGB values for your monitor. If you are using a CRT monitor the 
    result will be useful as an approximation but this is not true for TFT or 
    other monitor technologies.
*/
I1_API
I1_ResultType I1_GetTriStimulus(I1_DeviceHandle devHndl, float tristimulus[TRISTIMULUS_SIZE], I1_Integer index);


/** @brief Get all densities (CMYK) of a previously triggered measurement
    @param[in]  devHndl handle to the device
    @param[out] densities pointer to the resulting array. Must be large enough 
                to hold 4 floating-point values, and cannot be null
    @param[out] autoDensityIndex pointer to the autoDensityIndex which will 
                yield the actual auto density. If null is passed as input, the 
                auto density will not be calculated
    @param[in]  index zero-based index of the densities. For spot measurement 
                results use zero
    @return eNoError on success
*/
I1_API
I1_ResultType I1_GetDensities(I1_DeviceHandle devHndl, float densities[DENSITY_SIZE], I1_Integer *autoDensityIndex, I1_Integer index);


/** @brief Get the density of a previously triggered measurement
    @param[in]  devHndl handle to the device
    @param[out] density pointer to the resulting array. Must be large enough to 
                hold 1 floating-point value, and cannot be null
    @param[in]  index zero-based index of the density to retrieve. For spot 
                measurement results use zero
    @return eNoError on success

    If DENSITY_FILTER_MODE_KEY has been set to DENSITY_FILTER_MODE_AUTO you can 
    use #I1_GetOption (devHndl, I1_LAST_AUTO_DENSITY_FILTER) to
    retrieve the actual density filter name.
*/
I1_API
I1_ResultType I1_GetDensity(I1_DeviceHandle devHndl, float *density, I1_Integer index);


/** @brief Set the substrate reference spectrum for tristimulus and density calculations
    @param[in]  devHndl handle to the device
    @param[in]  spectrum of the substrate. Must not be null
    @return eNoError on success

    Activate the substrate afterwards whith WHITE_BASE_PAPER, disable it with WHITE_BASE_ABSOLUTE.
*/
I1_API
I1_ResultType I1_SetSubstrate(I1_DeviceHandle devHndl, const float spectrum[SPECTRUM_SIZE]);


/** @brief Set the reference data row of a chart for the next chart correlation
    @param[in] devHndl handle to the device. Must not be null
    @param[in] referenceChartLine array of Tristimulus or Density reference 
               values for the line.
               e.g. {R0, G0, B0, R1, G1, B1, ...} or {C0, M0, Y0, K0, C1, M1, ...}. Must not be null
    @param[in] lineSize number of patches in line
    @return eNoError on success

    Sets the reference values for the next patch correlation if the correlation 
    algorithm is activated (#I1_PATCH_RECOGNITION_CORRELATION).
    This method can be used only in #I1_REFLECTANCE_SCAN
    measurement mode with recognition correlation algorithm activated. The 
    reference line must be set before #I1_TriggerMeasurement is
    called. I1_TriggerMeasurement will then try to correlate the patches. So the 
    order of patches may be reversed when fetching the spectra/tristimulus/density 
    values. Use the #I1_REFERENCE_CHART_COLOR_SPACE_KEY key to set
    the color space for the reference line data. The color space may be RGB, Lab 
    or CMYK. This must be done before setting the reference line. For 
    Tristimulus reference data, the array size must be 3 times the number of 
    reference patches. For density, the array size must be 4 times the number of 
    reference patches.

    @code
      // Switch to reflectance scan, calibrate and activate correlation
      I1_SetOption(devHndl, I1_MEASUREMENT_MODE, I1_REFLECTANCE_SCAN);
      I1_Calibrate(devHndl);
      I1_SetOption(devHndl, I1_PATCH_RECOGNITION_KEY, I1_PATCH_RECOGNITION_CORRELATION); 

      // Set color space of reference chart line (RGB, CMYK or Lab)
      I1_SetOption(devHndl, I1_REFERENCE_CHART_COLOR_SPACE_KEY, I1_REFERENCE_CHART_CMYK);

      // Set data of reference chart line
      I1_SetReferenceChartLine(devHndl, refLabValues, cNrOfReferencePatches);

      // Trigger measurement and fetch data
      I1_TriggerMeasurement(devHndl);
      nrOfSamples = I1_GetNumberOfAvailableSamples(devHndl);
      I1_GetTriStimulus(tristimulus, i); 
    @endcode
*/
I1_API
I1_ResultType I1_SetReferenceChartLine(I1_DeviceHandle devHndl, const float *referenceChartLine, I1_Integer lineSize);

/*@} end results*/



/******************************************************************************/
/** @defgroup event Device Events
    @{
*/

/** @brief This emumeration is used to specify the event type. */
enum {
  eI1ProArrival                 = 0x11,   /**< i1Pro plugged-in */
  eI1ProDeparture               = 0x12,   /**< i1Pro unplugged */

  eI1ProButtonPressed           = 0x01,   /**< measure button pressed on i1Pro */
  eI1ProScanReadyToMove         = 0x02,   /**< in scan mode with Tungsten filament lamp: i1Pro can be moved now. Use this event to beep, flash screen, etc. to signal user that he now can start to move the device */
  eI1ProLampRestore             = 0x03    /**< calibration detected a nonstandard lamp condition. Restoring the standard lamp condition adds around 120 seconds to the calibration process. If this event is emitted, inform user that calibration will take longer than usual #I1_Calibrate() */
};
typedef I1_UInteger I1_DeviceEvent;

/** @brief Callback signature of a device event handler function
    @param[in] devHndl handle to the device
    @param[in] event event type, e.g. eI1ProButtonPressed
    @param[in] context the context which was registered with the handler

    The callback can be named as you like, so long as the signature matches FPtr_I1_DeviceEventHandler.
*/
typedef void (I1_CALLING_CONVENTION *FPtr_I1_DeviceEventHandler)(I1_DeviceHandle devHndl, I1_DeviceEvent event, void *context);

/** @brief Registers a device event handler callback function
    @param[in] handler a pointer to the event handler callback function.
               Or NULL if a registered handler should be removed
    @param[in] context a context for the callbacks use. May be NULL
    @return the previously installed event handler function or NULL if none has been installed yet

    In case of a device event, this handler is invoked in its own thread. Events will be queued.
    @note A second call to the SDK from a different thread is blocked.
    eg. eI1ProScanReadyToMove is emitted by I1_TriggerMeasurement(). Which means,
    you can't make another SDK call inside your event handler until I1_TriggerMeasurement()
    has exit in the main thread. Same for eI1ProLampRestore.

    @code
    void MyDeviceEventFunction(I1_DeviceHandle devHndl, I1_DeviceEvent event, void *context) {
      MyDeviceClass *dev = reinterpret_cast<MyDeviceClass *>(context);
      switch(event) {
        case eI1ProButtonPressed:   dev->MyButtonPressedAction(devHndl);    break;
        case eI1ProScanReadyToMove: Beep(2140, 75);                         break;
        case eI1ProLampRestore:     dev->InformUserLongCalibration();       break;
        case eI1ProArrival:         dev->MyDeviceArrivalAction(devHndl);    break;
        case eI1ProDeparture:       dev->MyDeviceDepartureAction(devHndl);  break;
      }
    }

    MyDeviceClass *obj;  // Filled in elsewhere
    I1_RegisterDeviceEventHandler(MyDeviceEventFunction, obj);
    @endcode
*/
I1_API
FPtr_I1_DeviceEventHandler I1_RegisterDeviceEventHandler(FPtr_I1_DeviceEventHandler handler, void *context);

/*@} end event*/



/******************************************************************************/
/******************************************************************************/
/*
    The FPtr_I1_XXX typedefs (e.g. FPtr_I1_Calibrate) are declared to 
    simplify the process of getting a reference to the desired method(s) while 
    dynamic loading this library.
*/
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetDevices)(I1_DeviceHandle**, I1_UInteger*);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_OpenDevice)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_CloseDevice)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_SetGlobalOption)(const char*, const char*);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetGlobalOption)(const char*, char*, I1_UInteger*);
typedef const char*   (I1_CALLING_CONVENTION *FPtr_I1_GetGlobalOptionD)(const char*);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_SetOption)(I1_DeviceHandle, const char*, const char*);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetOption)(I1_DeviceHandle, const char*, char*, I1_UInteger*);
typedef const char*   (I1_CALLING_CONVENTION *FPtr_I1_GetOptionD)(I1_DeviceHandle, const char*);
typedef I1_ConnectionStatusType (I1_CALLING_CONVENTION *FPtr_I1_GetConnectionStatus)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetButtonStatusD)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_Calibrate)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_TriggerMeasurement)(I1_DeviceHandle);
typedef I1_Integer    (I1_CALLING_CONVENTION *FPtr_I1_GetNumberOfAvailableSamples)(I1_DeviceHandle);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetSpectrum)(I1_DeviceHandle, float[SPECTRUM_SIZE], I1_Integer);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetTriStimulus)(I1_DeviceHandle, float[TRISTIMULUS_SIZE], I1_Integer);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetDensities)(I1_DeviceHandle, float[DENSITY_SIZE], I1_Integer*, I1_Integer);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_GetDensity)(I1_DeviceHandle, float*, I1_Integer);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_SetSubstrate)(I1_DeviceHandle, const float[SPECTRUM_SIZE]);
typedef I1_ResultType (I1_CALLING_CONVENTION *FPtr_I1_SetReferenceChartLine)(I1_DeviceHandle, const float*, I1_Integer);
typedef FPtr_I1_DeviceEventHandler (I1_CALLING_CONVENTION *FPtr_I1_RegisterDeviceEventHandler)(FPtr_I1_DeviceEventHandler, void*);


#ifdef __cplusplus
  }
#endif

#endif /*I1PRO_H*/
