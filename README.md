# Gentec Beamage 4M IR Camera - Python Interface

Python interface for the Gentec Beamage 4M IR beam profiling camera, providing programmatic access to beam capture and analysis capabilities.

## Overview

This package provides a Python wrapper for the Gentec Beamage SDK, enabling automated beam profiling and data acquisition for infrared laser characterization. The interface supports:

- **Automated beam capture** with configurable exposure settings
- **Real-time beam analysis** (4-sigma diameter, centroid position, FPS)
- **FITS file output** with comprehensive metadata headers
- **NumPy array integration** for seamless data processing
- **Matplotlib visualization** with automatic beam analysis plots

Developed for the CREOL Astrophotonics Lab at the University of Central Florida.

## Requirements

### Hardware & Software Dependencies

1. **PC-BEAMAGE Software** (Gentec-EO)
   - Download and install from [Gentec-EO website](https://www.gentec-eo.com)
   - Includes necessary USB drivers for camera communication
   - Verify camera connectivity using the PC-BEAMAGE GUI before using this tool

2. **Beamage SDK** (C# DLL)
   - Obtain SDK from Gentec-EO (typically provided via email or download link)
   - Extract to a known location (default: `./Example_Beamage_SDK_CSharp_V1.02.02/`)

### Python Dependencies

```bash
pip install pythonnet numpy matplotlib astropy
```

**Package Versions:**
- `pythonnet` - .NET interoperability for Python
- `numpy` - Array operations and data handling
- `matplotlib` - Visualization and plotting
- `astropy` - FITS file I/O with proper astronomical data formats

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd gentec-camera
```

### 2. Install Python Dependencies

```bash
pip install pythonnet numpy matplotlib astropy
```

### 3. Unblock SDK DLL (Windows Security)

Windows blocks execution of DLLs downloaded from the internet by default. Unblock the SDK DLL using PowerShell:

```powershell
Unblock-File -Path ".\Example_Beamage_SDK_CSharp_V1.02.02\3. DLL File\BeamageSDK.dll"
```

This grants execution permissions for the SDK library.

### 4. Verify Setup

Test camera connectivity:

```bash
python main.py --auto-exposure --frames 1
```

## Usage

### Command-Line Interface

The main script provides a comprehensive CLI for beam capture:

```bash
# Auto-exposure, capture 10 frames
python main.py --auto-exposure --frames 10

# Manual exposure (50.5 ms), save to custom file
python main.py --exposure 50.5 --output beam_profile.fits

# Single frame capture without visualization
python main.py --exposure 100 --frames 1 --no-plot

# Specify camera by serial number
python main.py --serial 228451 --auto-exposure
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--exposure MS` | Manual exposure time in milliseconds (0.06-5000 ms) | Auto |
| `--auto-exposure` | Enable automatic exposure control | - |
| `--frames N` | Number of frames to capture | 5 |
| `--delay SEC` | Delay between frame captures (seconds) | 0.5 |
| `--output FILE` | Output filename (.fits, .npy, or .png) | `beamage_capture.fits` |
| `--no-plot` | Skip matplotlib visualization | - |
| `--save-all` | Save all captured frames (creates 3D array) | False |
| `--serial SN` | Camera serial number (for multi-camera setups) | First detected |
| `--dll PATH` | Custom path to BeamageSDK.dll | Auto-detected |
| `--timeout SEC` | Frame capture timeout | 5.0 |
| `--quiet`, `-q` | Suppress informational messages | - |
| `--verbose`, `-v` | Enable debug output | - |

### Python API

For programmatic control, import the `BeamageCamera` class:

```python
from main import BeamageCamera
from pathlib import Path

# Initialize camera
dll_path = Path("./Example_Beamage_SDK_CSharp_V1.02.02/3. DLL File/BeamageSDK.dll")
cam = BeamageCamera(dll_path=dll_path)

# Connect and configure
cam.connect()
cam.set_exposure(50.0)  # 50 ms exposure
cam.start()

# Capture frame
image = cam.capture(timeout=5.0)  # Returns numpy array (2048 × 2048)

# Get beam statistics
stats = cam.get_beam_stats()
print(f"Beam diameter: {stats['diameter_x']:.2f} µm × {stats['diameter_y']:.2f} µm")
print(f"Centroid: ({stats['centroid_x']:.1f}, {stats['centroid_y']:.1f})")

# Cleanup
cam.stop()
cam.disconnect()
```

### Context Manager Support

```python
with BeamageCamera(dll_path=dll_path) as cam:
    cam.connect()
    cam.set_auto_exposure(True)
    cam.start()
    
    image = cam.capture()
    # Camera automatically disconnects on exit
```

## Output Formats

### FITS Files (Recommended)

FITS output includes comprehensive metadata headers:

- **Acquisition parameters**: exposure time, detector type, serial number
- **Beam analysis**: 4-sigma diameter (X/Y), centroid position
- **Statistical data**: min/max/mean/std of pixel values
- **Wavelength calibration**: nominal 1550 nm, range 1495-1595 nm
- **Provenance**: capture timestamp, lab information, software version

### NumPy Arrays

Raw array data saved in `.npy` format for direct processing in Python/MATLAB.

### PNG Visualizations

Auto-generated plots include:
- Full sensor view with percentile-based scaling
- Zoomed region around beam peak
- Crosshair markers at peak intensity location

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| **Sensor Resolution** | 2048 × 2048 pixels |
| **Pixel Size** | 5.5 µm × 5.5 µm |
| **Wavelength Range** | 1495-1595 nm (optimized for 1550 nm) |
| **Exposure Range** | 0.06-5000 ms |
| **Data Type** | 32-bit integer |
| **SDK Version** | 1.2.0.2 |

## Troubleshooting

### Camera Not Detected

1. Verify USB connection
2. Confirm PC-BEAMAGE GUI can access the camera
3. Check Windows Device Manager for driver issues
4. Restart USB hub or computer if necessary

### DLL Load Errors

```
FileNotFoundError: BeamageSDK.dll not found
```

**Solution**: Verify DLL path in script or use `--dll` flag to specify location manually.

### DLL Execution Blocked

```
System.IO.FileLoadException: Operation is not supported
```

**Solution**: Run the `Unblock-File` PowerShell command (see Installation step 3).

### Frame Timeout Errors

```
TimeoutError: No image received within 5 seconds
```

**Solution**: 
- Increase timeout with `--timeout 10`
- Check if camera is receiving light (exposure may be too short)
- Verify camera is not in use by another application

### Python Environment Issues

If using Conda environments, ensure proper activation:

```bash
conda activate your-environment-name
python main.py --help
```

## Project Structure

```
gentec-camera/
├── main.py                          # Main CLI and BeamageCamera class
├── README.md                        # This file
├── beamage_capture.fits             # Example FITS output
├── beamage_capture.npy              # Example NumPy output
├── beamage_capture.png              # Example visualization
├── Beamage_.Net_Example_V1.00.08/   # C# named pipe example
└── Example_Beamage_SDK_CSharp_V1.02.02/
    └── 3. DLL File/
        └── BeamageSDK.dll           # Gentec SDK library
```

## Contributing

This tool was developed for the Dr. Eikenberry Research Group at CREOL, University of Central Florida. Contributions and issue reports are welcome via the repository issue tracker.

## License

Refer to Gentec-EO licensing terms for SDK usage. This wrapper code is provided as-is for academic research purposes.

## Acknowledgments

- **CREOL Astrophotonics Lab** - University of Central Florida
- **Gentec-EO** - Beamage SDK and hardware support
- **Dr. Eikenberry Research Group** - Research infrastructure and guidance
