"""
Python wrapper for the i1Pro SDK
Compatible with Python 3.11+
Uses numpy for data structures
"""

import ctypes
from ctypes import c_char_p, c_void_p, c_uint32, c_int32, c_float, POINTER, byref
from enum import IntEnum, IntFlag
import numpy as np
from typing import Optional, Tuple, List
import os


# Type definitions matching i1Pro.h
I1_Integer = c_int32
I1_UInteger = c_uint32
I1_DeviceHandle = c_void_p
I1_ResultType = c_uint32


class I1ResultType(IntEnum):
    """Result codes from i1Pro SDK"""
    eNoError = 0
    eException = 1
    eBadBuffer = 2
    eInvalidHandle = 9
    eInvalidArgument = 10
    eDeviceNotOpen = 11
    eDeviceNotConnected = 12
    eDeviceNotCalibrated = 13
    eNoDataAvailable = 14
    eNoMeasureModeSet = 15
    eNoReferenceChartLine = 17
    eNoSubstrateWhite = 18
    eNotLicensed = 19
    eDeviceAlreadyOpen = 20
    eDeviceAlreadyInUse = 51
    eDeviceCommunicationError = 52
    eUSBPowerProblem = 53
    eNotOnWhiteTile = 54
    eStripRecognitionFailed = 60
    eChartCorrelationFailed = 61
    eInsufficientMovement = 62
    eExcessiveMovement = 63
    eEarlyScanStart = 64
    eUserTimeout = 65
    eIncompleteScan = 66
    eDeviceNotMoved = 67
    eDeviceCorrupt = 71
    eWavelengthShift = 72


class I1ConnectionStatusType(IntEnum):
    """Connection status types"""
    eInvalidConnectionHandle = 0x00
    eI1ProClosed = 0x01
    eI1ProOpen = 0x03


class I1ButtonStatusType(IntEnum):
    """Button status types"""
    eButtonIsPressed = 1000
    eButtonNotPressed = 1001


class I1DeviceEvent(IntEnum):
    """Device event types"""
    eI1ProArrival = 0x11
    eI1ProDeparture = 0x12
    eI1ProButtonPressed = 0x01
    eI1ProScanReadyToMove = 0x02
    eI1ProLampRestore = 0x03


class MeasurementMode(IntEnum):
    """Measurement modes for i1Pro"""
    EMISSION_SPOT = 0
    REFLECTANCE_SPOT = 1
    DUAL_REFLECTANCE_SPOT = 2
    REFLECTANCE_SCAN = 3
    DUAL_REFLECTANCE_SCAN = 4
    AMBIENT_LIGHT_SPOT = 5
    AMBIENT_LIGHT_SCAN = 6


class Illumination(IntEnum):
    """Illumination types"""
    A = 0
    B = 1
    C = 2
    D50 = 3
    D55 = 4
    D65 = 5
    D75 = 6
    F2 = 7
    F7 = 8
    F11 = 9
    EMISSION = 10


class Observer(IntEnum):
    """Observer types"""
    TWO_DEGREE = 0
    TEN_DEGREE = 1


# SDK Constants
SPECTRUM_SIZE = 36  # 380-730nm in 10nm steps
TRISTIMULUS_SIZE = 3  # X, Y, Z or x, y, Y
DENSITY_SIZE = 4  # C, M, Y, K

# Measurement mode strings for SDK
_MEASUREMENT_MODE_STRINGS = {
    MeasurementMode.EMISSION_SPOT: b"EmissionSpot",
    MeasurementMode.REFLECTANCE_SPOT: b"ReflectanceSpot",
    MeasurementMode.DUAL_REFLECTANCE_SPOT: b"DualReflectanceSpot",
    MeasurementMode.REFLECTANCE_SCAN: b"ReflectanceScan",
    MeasurementMode.DUAL_REFLECTANCE_SCAN: b"DualReflectanceScan",
    MeasurementMode.AMBIENT_LIGHT_SPOT: b"AmbientLightSpot",
    MeasurementMode.AMBIENT_LIGHT_SCAN: b"AmbientLightScan",
}

# Illumination strings for SDK
_ILLUMINATION_STRINGS = {
    Illumination.A: b"A",
    Illumination.B: b"B",
    Illumination.C: b"C",
    Illumination.D50: b"D50",
    Illumination.D55: b"D55",
    Illumination.D65: b"D65",
    Illumination.D75: b"D75",
    Illumination.F2: b"F2",
    Illumination.F7: b"F7",
    Illumination.F11: b"F11",
    Illumination.EMISSION: b"Emission",
}

# Observer strings for SDK
_OBSERVER_STRINGS = {
    Observer.TWO_DEGREE: b"TwoDegree",
    Observer.TEN_DEGREE: b"TenDegree",
}


def get_default_dll_path() -> str:
    """
    Get the default path to the i1Pro DLL.
    
    Searches in the following order:
    1. i1Profiler installation directory (preferred for working 32-bit DLL)
    2. dlls/ directory relative to the package root
    3. Same directory as this module
    4. Current working directory
    
    Returns:
        Path to the DLL file
    """
    import struct
    is_32bit = struct.calcsize("P") * 8 == 32
    
    # Get the directory containing this module
    module_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the package root (two levels up: src/xRite -> xRite project root)
    package_root = os.path.dirname(os.path.dirname(module_dir))
    
    # For 32-bit Python, prefer the i1Profiler installation (known working DLL)
    if is_32bit:
        # Check i1Profiler installation paths
        i1profiler_paths = [
            r"C:\Program Files (x86)\X-Rite\Devices\i1pro\i1Pro.dll",
            r"C:\Program Files\X-Rite\Devices\i1pro\i1Pro.dll",
        ]
        for dll_path in i1profiler_paths:
            if os.path.exists(dll_path):
                return dll_path
    
    # Check in dlls/ directory relative to package root
    if is_32bit:
        dll_path = os.path.join(package_root, "dlls", "i1Pro.dll")
        if os.path.exists(dll_path):
            return dll_path
    
    dll_path = os.path.join(package_root, "dlls", "i1Pro64.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    # Check for 32-bit DLL in dlls folder
    dll_path = os.path.join(package_root, "dlls", "i1Pro.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    # Check same directory as module
    if is_32bit:
        dll_path = os.path.join(module_dir, "i1Pro.dll")
        if os.path.exists(dll_path):
            return dll_path
    
    dll_path = os.path.join(module_dir, "i1Pro64.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    dll_path = os.path.join(module_dir, "i1Pro.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    # Check current working directory
    if is_32bit:
        dll_path = os.path.join(os.getcwd(), "i1Pro.dll")
        if os.path.exists(dll_path):
            return dll_path
    
    dll_path = os.path.join(os.getcwd(), "i1Pro64.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    dll_path = os.path.join(os.getcwd(), "i1Pro.dll")
    if os.path.exists(dll_path):
        return dll_path
    
    # Return default path based on architecture (will fail if not found)
    if is_32bit:
        return r"C:\Program Files (x86)\X-Rite\Devices\i1pro\i1Pro.dll"
    return os.path.join(package_root, "dlls", "i1Pro64.dll")


class I1ProException(Exception):
    """Exception for i1Pro SDK errors"""
    def __init__(self, result_code: I1ResultType, message: str = ""):
        self.result_code = result_code
        self.message = message
        super().__init__(f"i1Pro Error {result_code}: {message}")


class I1ProSDK:
    """Low-level wrapper for i1Pro SDK DLL"""
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize the SDK wrapper
        
        Args:
            dll_path: Path to i1Pro64.dll (or i1Pro.dll for 32-bit)
                     If None, searches in default locations
        """
        if dll_path is None:
            dll_path = get_default_dll_path()
        
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"i1Pro DLL not found at: {dll_path}")
        
        self.dll = ctypes.CDLL(dll_path)
        self._setup_functions()
    
    def _setup_functions(self):
        """Setup function signatures for all SDK functions"""
        
        # I1_GetDevices
        # Signature: I1_GetDevices(I1_DeviceHandle **devices, I1_UInteger *count)
        # I1_DeviceHandle is a pointer (struct I1_Device_ *), so we need pointer-to-pointer
        # The SDK fills *devices with a pointer to its internal static array of handles
        self.dll.I1_GetDevices.argtypes = [
            POINTER(POINTER(c_void_p)),  # I1_DeviceHandle** - pointer to pointer
            POINTER(I1_UInteger)          # I1_UInteger* - pointer to count
        ]
        self.dll.I1_GetDevices.restype = I1_ResultType
        
        # I1_OpenDevice
        self.dll.I1_OpenDevice.argtypes = [I1_DeviceHandle]
        self.dll.I1_OpenDevice.restype = I1_ResultType
        
        # I1_CloseDevice
        self.dll.I1_CloseDevice.argtypes = [I1_DeviceHandle]
        self.dll.I1_CloseDevice.restype = I1_ResultType
        
        # I1_SetGlobalOption
        self.dll.I1_SetGlobalOption.argtypes = [c_char_p, c_char_p]
        self.dll.I1_SetGlobalOption.restype = I1_ResultType
        
        # I1_GetGlobalOption
        self.dll.I1_GetGlobalOption.argtypes = [c_char_p, c_char_p, POINTER(I1_UInteger)]
        self.dll.I1_GetGlobalOption.restype = I1_ResultType
        
        # I1_SetOption
        self.dll.I1_SetOption.argtypes = [I1_DeviceHandle, c_char_p, c_char_p]
        self.dll.I1_SetOption.restype = I1_ResultType
        
        # I1_GetOption
        self.dll.I1_GetOption.argtypes = [I1_DeviceHandle, c_char_p, c_char_p, POINTER(I1_UInteger)]
        self.dll.I1_GetOption.restype = I1_ResultType
        
        # I1_GetConnectionStatus
        self.dll.I1_GetConnectionStatus.argtypes = [I1_DeviceHandle]
        self.dll.I1_GetConnectionStatus.restype = I1_UInteger
        
        # I1_GetButtonStatusD
        self.dll.I1_GetButtonStatusD.argtypes = [I1_DeviceHandle]
        self.dll.I1_GetButtonStatusD.restype = I1_UInteger
        
        # I1_Calibrate
        self.dll.I1_Calibrate.argtypes = [I1_DeviceHandle]
        self.dll.I1_Calibrate.restype = I1_ResultType
        
        # I1_TriggerMeasurement
        self.dll.I1_TriggerMeasurement.argtypes = [I1_DeviceHandle]
        self.dll.I1_TriggerMeasurement.restype = I1_ResultType
        
        # I1_GetNumberOfAvailableSamples
        self.dll.I1_GetNumberOfAvailableSamples.argtypes = [I1_DeviceHandle]
        self.dll.I1_GetNumberOfAvailableSamples.restype = I1_Integer
        
        # I1_GetSpectrum
        self.dll.I1_GetSpectrum.argtypes = [
            I1_DeviceHandle,
            POINTER(c_float * SPECTRUM_SIZE),
            I1_Integer
        ]
        self.dll.I1_GetSpectrum.restype = I1_ResultType
        
        # I1_GetTriStimulus
        self.dll.I1_GetTriStimulus.argtypes = [
            I1_DeviceHandle,
            POINTER(c_float * TRISTIMULUS_SIZE),
            I1_Integer
        ]
        self.dll.I1_GetTriStimulus.restype = I1_ResultType
        
        # I1_GetDensities
        self.dll.I1_GetDensities.argtypes = [
            I1_DeviceHandle,
            POINTER(c_float * DENSITY_SIZE),
            POINTER(I1_Integer),
            I1_Integer
        ]
        self.dll.I1_GetDensities.restype = I1_ResultType
        
        # I1_GetDensity
        self.dll.I1_GetDensity.argtypes = [
            I1_DeviceHandle,
            POINTER(c_float),
            I1_Integer
        ]
        self.dll.I1_GetDensity.restype = I1_ResultType


class I1Pro:
    """High-level Python wrapper for i1Pro colorimeter"""
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize i1Pro device
        
        Args:
            dll_path: Optional path to i1Pro DLL
        """
        self.sdk = I1ProSDK(dll_path)
        self.device_handle: Optional[I1_DeviceHandle] = None
        self.is_open = False
        self.is_calibrated = False
        self.measurement_mode: Optional[MeasurementMode] = None
        
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def _check_result(self, result: int):
        """Check SDK result code and raise exception if error"""
        if result != I1ResultType.eNoError:
            error_text = self.get_last_error_text()
            raise I1ProException(I1ResultType(result), error_text)
    
    def get_last_error_text(self) -> str:
        """Get last error description"""
        buffer = ctypes.create_string_buffer(256)
        size = I1_UInteger(256)
        self.sdk.dll.I1_GetGlobalOption(
            b"LastErrorText",
            buffer,
            byref(size)
        )
        return buffer.value.decode('utf-8')
    
    def get_devices(self) -> int:
        """
        Get number of connected i1Pro devices
        
        Returns:
            Number of connected devices
        """
        # I1_GetDevices signature: I1_GetDevices(I1_DeviceHandle **devices, I1_UInteger *count)
        # I1_DeviceHandle is already a pointer (struct I1_Device_ *)
        # So I1_DeviceHandle** is a pointer to a pointer
        # The SDK writes to *devices the address of its internal static array of handles
        
        # Create a pointer variable that will receive the array address
        # This is equivalent to: I1_DeviceHandle *devices_array = NULL;
        # Then passing &devices_array to the function
        devices_array = POINTER(c_void_p)()  # NULL pointer to c_void_p (device handle)
        count = I1_UInteger(0)
        
        # Pass address of our pointer variable so SDK can fill it
        result = self.sdk.dll.I1_GetDevices(byref(devices_array), byref(count))
        self._check_result(result)
        
        if count.value > 0 and devices_array:
            # devices_array now points to the SDK's internal array of device handles
            # Access the first device handle (index 0)
            self.device_handle = devices_array[0]
        
        return count.value
    
    def open(self, device_index: int = 0) -> bool:
        """
        Open a device connection
        
        Args:
            device_index: Index of device to open (default: 0)
            
        Returns:
            True if successful
        """
        if self.is_open:
            return True
        
        # Get devices
        num_devices = self.get_devices()
        if num_devices == 0:
            raise I1ProException(I1ResultType.eDeviceNotConnected, 
                               "No i1Pro devices connected")
        
        if device_index >= num_devices:
            raise I1ProException(I1ResultType.eInvalidArgument,
                               f"Device index {device_index} out of range (0-{num_devices-1})")
        
        # Open the device
        result = self.sdk.dll.I1_OpenDevice(self.device_handle)
        self._check_result(result)
        
        self.is_open = True
        self.is_calibrated = False
        return True
    
    def close(self):
        """Close device connection"""
        if self.is_open and self.device_handle:
            self.sdk.dll.I1_CloseDevice(self.device_handle)
            self.is_open = False
            self.is_calibrated = False
            self.device_handle = None
    
    def set_measurement_mode(self, mode: MeasurementMode):
        """
        Set measurement mode
        
        Args:
            mode: Measurement mode to set
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen, 
                               "Device not open")
        
        mode_str = _MEASUREMENT_MODE_STRINGS[mode]
        result = self.sdk.dll.I1_SetOption(
            self.device_handle,
            b"MeasurementMode",
            mode_str
        )
        self._check_result(result)
        
        self.measurement_mode = mode
        self.is_calibrated = False  # Mode change invalidates calibration
    
    def set_illumination(self, illumination: Illumination):
        """
        Set illumination type
        
        Args:
            illumination: Illumination type
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        illum_str = _ILLUMINATION_STRINGS[illumination]
        result = self.sdk.dll.I1_SetOption(
            self.device_handle,
            b"Colorimetric.Illumination",
            illum_str
        )
        self._check_result(result)
    
    def set_observer(self, observer: Observer):
        """
        Set observer type
        
        Args:
            observer: Observer type (2° or 10°)
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        obs_str = _OBSERVER_STRINGS[observer]
        result = self.sdk.dll.I1_SetOption(
            self.device_handle,
            b"Colorimetric.Observer",
            obs_str
        )
        self._check_result(result)
    
    def calibrate(self) -> bool:
        """
        Calibrate the device
        Place device on white tile before calling
        
        Returns:
            True if successful
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        result = self.sdk.dll.I1_Calibrate(self.device_handle)
        self._check_result(result)
        
        self.is_calibrated = True
        return True
    
    def trigger_measurement(self) -> bool:
        """
        Trigger a measurement
        
        Returns:
            True if successful
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        if not self.is_calibrated:
            raise I1ProException(I1ResultType.eDeviceNotCalibrated,
                               "Device not calibrated")
        
        result = self.sdk.dll.I1_TriggerMeasurement(self.device_handle)
        self._check_result(result)
        
        return True
    
    def get_number_of_samples(self) -> int:
        """
        Get number of available samples from last measurement
        
        Returns:
            Number of samples (1 for spot, multiple for scan)
        """
        if not self.is_open:
            return 0
        
        return self.sdk.dll.I1_GetNumberOfAvailableSamples(self.device_handle)
    
    def get_spectrum(self, index: int = 0) -> np.ndarray:
        """
        Get spectral data from measurement
        
        Args:
            index: Sample index (default: 0 for spot measurements)
            
        Returns:
            numpy array of 36 spectral values (380-730nm in 10nm steps)
            - For reflectance mode: values in % (0-100)
            - For emission mode: relative values (scale varies)
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        spectrum = (c_float * SPECTRUM_SIZE)()
        result = self.sdk.dll.I1_GetSpectrum(
            self.device_handle,
            byref(spectrum),
            I1_Integer(index)
        )
        self._check_result(result)
        
        # Convert to numpy array and ensure no negative values
        spec_array = np.array(spectrum, dtype=np.float32)
        spec_array[spec_array < 0] = 0.0
        
        # In reflectance mode, SDK returns values as fractions (0-1)
        # but Y values as percentages (0-100). Scale spectrum to match.
        # Check if we're in reflectance mode by testing spectrum range
        if self.measurement_mode in [MeasurementMode.REFLECTANCE_SPOT,
                                     MeasurementMode.REFLECTANCE_SCAN,
                                     MeasurementMode.DUAL_REFLECTANCE_SPOT,
                                     MeasurementMode.DUAL_REFLECTANCE_SCAN]:
            # Scale from 0-1 to 0-100 to match Y percentage
            spec_array = spec_array * 100.0
        
        return spec_array
    
    def get_tristimulus(self, index: int = 0) -> np.ndarray:
        """
        Get tristimulus values from measurement (x, y, Y for xyY or X, Y, Z)
        
        Args:
            index: Sample index (default: 0 for spot measurements)
            
        Returns:
            numpy array of 3 tristimulus values
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        # Set color space to CIE xyY
        result = self.sdk.dll.I1_SetOption(
            self.device_handle,
            b"ColorSpaceDescription.Type",
            b"CIExyY"
        )
        self._check_result(result)
        
        tristimulus = (c_float * TRISTIMULUS_SIZE)()
        result = self.sdk.dll.I1_GetTriStimulus(
            self.device_handle,
            byref(tristimulus),
            I1_Integer(index)
        )
        self._check_result(result)
        
        return np.array(tristimulus, dtype=np.float32)
    
    def get_xyY(self, index: int = 0) -> Tuple[float, float, float]:
        """
        Get xyY color coordinates
        
        Args:
            index: Sample index
            
        Returns:
            Tuple of (x, y, Y)
        """
        tristimulus = self.get_tristimulus(index)
        return tuple(tristimulus)
    
    def measure_xyY(self) -> Tuple[float, float, float]:
        """
        Perform a complete measurement and return xyY
        
        Returns:
            Tuple of (x, y, Y) coordinates
        """
        self.trigger_measurement()
        return self.get_xyY()
    
    def measure_spectrum(self) -> np.ndarray:
        """
        Perform a complete measurement and return spectrum
        
        Returns:
            numpy array of 36 spectral values
        """
        self.trigger_measurement()
        return self.get_spectrum()
    
    def measure_xyY_and_spectrum(self) -> Tuple[Tuple[float, float, float], np.ndarray]:
        """
        Perform a complete measurement and return both xyY and spectrum
        
        Returns:
            Tuple of (xyY tuple, spectrum array)
        """
        self.trigger_measurement()
        xyY = self.get_xyY()
        spectrum = self.get_spectrum()
        return xyY, spectrum
    
    def is_button_pressed(self) -> bool:
        """
        Check if device button is pressed
        
        Returns:
            True if button pressed
        """
        if not self.is_open:
            return False
        
        status = self.sdk.dll.I1_GetButtonStatusD(self.device_handle)
        return status == I1ButtonStatusType.eButtonIsPressed
    
    def wait_for_button(self):
        """Wait for user to press button on device"""
        import time
        print("Press the i1Pro button...")
        while not self.is_button_pressed():
            time.sleep(0.1)
        # Wait for release
        while self.is_button_pressed():
            time.sleep(0.1)
    
    def get_wavelengths(self) -> np.ndarray:
        """
        Get wavelength array corresponding to spectrum measurements
        
        Returns:
            numpy array of 36 wavelengths (380-730nm in 10nm steps)
        """
        return np.arange(380, 731, 10, dtype=np.float32)
    
    def get_serial_number(self) -> str:
        """
        Get device serial number
        
        Returns:
            Serial number string
        """
        if not self.is_open:
            raise I1ProException(I1ResultType.eDeviceNotOpen,
                               "Device not open")
        
        buffer = ctypes.create_string_buffer(256)
        size = I1_UInteger(256)
        result = self.sdk.dll.I1_GetOption(
            self.device_handle,
            b"SerialNumber",
            buffer,
            byref(size)
        )
        self._check_result(result)
        
        return buffer.value.decode('utf-8')
    
    def get_sdk_version(self) -> str:
        """
        Get SDK version
        
        Returns:
            SDK version string
        """
        buffer = ctypes.create_string_buffer(256)
        size = I1_UInteger(256)
        result = self.sdk.dll.I1_GetGlobalOption(
            b"SDKVersion",
            buffer,
            byref(size)
        )
        self._check_result(result)
        
        return buffer.value.decode('utf-8')


def main():
    """Example usage"""
    try:
        # Create i1Pro instance
        with I1Pro() as device:
            print(f"SDK Version: {device.get_sdk_version()}")
            
            # Get number of devices
            num_devices = device.get_devices()
            print(f"Number of devices connected: {num_devices}")
            
            if num_devices == 0:
                print("No i1Pro devices found!")
                return
            
            # Open device
            device.open()
            print(f"Device opened. Serial: {device.get_serial_number()}")
            
            # Set measurement mode
            device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
            device.set_observer(Observer.TWO_DEGREE)
            
            # Calibrate
            print("\nPlace device on white tile and press Enter...")
            input()
            device.calibrate()
            print("Calibrated!")
            
            # Measure
            print("\nReady to measure. Press button on device...")
            device.wait_for_button()
            
            xyY, spectrum = device.measure_xyY_and_spectrum()
            
            print(f"\nMeasurement results:")
            print(f"xyY: x={xyY[0]:.4f}, y={xyY[1]:.4f}, Y={xyY[2]:.2f}")
            print(f"\nSpectrum (380-730nm in 10nm steps):")
            wavelengths = device.get_wavelengths()
            for wl, val in zip(wavelengths, spectrum):
                print(f"  {int(wl)}nm: {val:.6f}")
    
    except I1ProException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
