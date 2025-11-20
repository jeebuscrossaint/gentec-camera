"""
Gentec Beamage 4M IR Camera - Windows Python Wrapper
Serial: 228451

SETUP INSTRUCTIONS:
===================

1. Download & Install PC-BEAMAGE Software + Drivers:
   https://www.gentec-eo.com/fr/diagnostic-de-faisceau-laser/profileurs-faisceaux
   (Go to Resources tab -> Downloads -> Latest PC-BEAMAGE + Drivers)

2. Test camera works with PC-BEAMAGE GUI first
   - Plug in camera via USB3
   - Launch PC-BEAMAGE
   - Verify you can see live image

3. Download BEAMAGE SDK:
   https://www.gentec-eo.com/dwl/software/Example_Beamage_SDK_CSharp_V1.02.02.zip
   
4. Extract and locate BeamageSDK.dll (usually in the bin folder)

5. Install Python dependencies:
   pip install pythonnet numpy matplotlib

6. Update DLL_PATH below to point to your BeamageSDK.dll

7. Run this script!

USAGE:
======
python main.py --exposure=92.19 --gain=1
python main.py --auto-exposure
python main.py --exposure=100 --gain=2 --frames=10

"""

import clr
import sys
import numpy as np
from pathlib import Path
from typing import Optional, Dict
import logging
import time
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Path to BeamageSDK.dll (relative to script location)
# ============================================================================
import os
SCRIPT_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd()
DLL_PATH = SCRIPT_DIR / "Example_Beamage_SDK_CSharp_V1.02.02" / "3. DLL File" / "BeamageSDK.dll"

# Or set absolute path:
# DLL_PATH = r"C:\full\path\to\BeamageSDK.dll"
# ============================================================================


class BeamageCamera:
    """
    Python wrapper for Gentec Beamage 4M IR camera
    Simple interface for exposure control and image capture
    """
    
    def __init__(self, dll_path: str = DLL_PATH, serial_number: str = "228451"):
        """
        Initialize camera
        
        Args:
            dll_path: Path to BeamageSDK.dll
            serial_number: Camera serial number (default: 228451)
        """
        self.serial_number = serial_number
        self.camera_index = None
        self.is_connected = False
        
        # Load the DLL
        dll_path = Path(dll_path)
        if not dll_path.exists():
            raise FileNotFoundError(
                f"BeamageSDK.dll not found at {dll_path}\n"
                f"Please update DLL_PATH in the script!"
            )
        
        sys.path.append(str(dll_path.parent))
        clr.AddReference(str(dll_path.stem))
        
        # Import SDK
        from BeamageApi import BSDK
        self.sdk = BSDK()
        
        # Camera specs
        self.width = 2048
        self.height = 2048
        self.pixel_size = 5.5  # um
        
        logger.info(f"SDK initialized (version: {self.sdk.GetVersion()})")
    
    def connect(self, camera_index: int = 0) -> bool:
        """
        Detect and connect to camera
        
        Args:
            camera_index: Which camera to connect to (0 = first)
        
        Returns:
            bool: True if successful
        """
        try:
            # Detect cameras
            self.sdk.Detect()
            
            if self.sdk.cameras.Count == 0:
                logger.error("No cameras detected! Check USB connection.")
                return False
            
            logger.info(f"Found {self.sdk.cameras.Count} camera(s)")
            
            # List all cameras
            for i in range(self.sdk.cameras.Count):
                serial = self.sdk.cameras[i].Properties.GetSerialNumber()
                is_4m = self.sdk.cameras[i].Properties.Is4mSensor()
                model = "Beamage-4M" if is_4m else "Beamage-3.0"
                logger.info(f"  [{i}] {model} S/N:{serial}")
            
            # Connect to specified camera
            if camera_index >= self.sdk.cameras.Count:
                logger.error(f"Camera index {camera_index} out of range")
                return False
            
            self.camera_index = camera_index
            self.sdk.cameras[self.camera_index].Connect()
            self.is_connected = True
            
            serial = self.sdk.cameras[self.camera_index].Properties.GetSerialNumber()
            logger.info(f"✓ Connected to camera {camera_index} (S/N:{serial})")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def start(self):
        """Start continuous image capture"""
        if not self.is_connected:
            raise RuntimeError("Not connected! Call connect() first")
        
        self.sdk.cameras[self.camera_index].Run()
        logger.info("Started capture")
    
    def stop(self):
        """Stop image capture"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        self.sdk.cameras[self.camera_index].StopRun()
        logger.info("Stopped capture")
    
    def set_exposure(self, time_ms: float):
        """
        Set exposure time (manual mode)
        
        Args:
            time_ms: Exposure time in milliseconds (0.06 to 5000)
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        if not (0.06 <= time_ms <= 5000):
            raise ValueError("Exposure must be 0.06-5000 ms")
        
        # Disable auto exposure first
        self.sdk.cameras[self.camera_index].SetToAutoExposure(False)
        self.sdk.cameras[self.camera_index].SetExposureTime(float(time_ms))
        logger.info(f"Set exposure: {time_ms} ms")
    
    def set_auto_exposure(self, enable: bool = True):
        """
        Enable/disable auto exposure
        
        Args:
            enable: True for auto, False for manual
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        self.sdk.cameras[self.camera_index].SetToAutoExposure(enable)
        logger.info(f"Auto exposure: {'ON' if enable else 'OFF'}")
    
    def get_exposure(self) -> float:
        """Get current exposure time in ms"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        return float(self.sdk.cameras[self.camera_index].Settings.exposureTime)
    
    def set_gain(self, gain: int):
        """
        Set camera gain
        
        Args:
            gain: Gain value (typically 1-4, check SDK docs for your model)
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        try:
            self.sdk.cameras[self.camera_index].SetGain(int(gain))
            logger.info(f"Set gain: {gain}")
        except Exception as e:
            logger.error(f"Failed to set gain: {e}")
            raise
    
    def get_gain(self) -> int:
        """Get current gain value"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        try:
            return int(self.sdk.cameras[self.camera_index].Settings.gain)
        except:
            logger.warning("Could not read gain value")
            return -1
    
    def capture(self) -> np.ndarray:
        """
        Capture single image
        
        Returns:
            np.ndarray: Image as 2D array (size depends on ROI settings)
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        # Get raw image buffer
        img_data = self.sdk.cameras[self.camera_index].Image.GetImage()
        
        # Convert to numpy array
        img_array = np.array(list(img_data), dtype=np.int32)
        
        # Get actual dimensions from SDK
        width = self.sdk.cameras[self.camera_index].Image.width
        height = self.sdk.cameras[self.camera_index].Image.height
        
        # The SDK always returns full sensor data (2048x2048)
        # but reports ROI dimensions, so we need to reshape to actual data size
        total_pixels = len(img_array)
        actual_width = 2048  # Beamage 4M sensor width
        actual_height = total_pixels // actual_width
        
        img_2d = img_array.reshape((actual_height, actual_width))
        
        logger.debug(f"Captured: {actual_width}x{actual_height} "
                    f"(SDK reports {width}x{height})")
        
        return img_2d
    
    def get_beam_stats(self) -> Dict:
        """
        Get beam analysis parameters
        
        Returns:
            dict: {
                'diameter_x': 4-sigma diameter X (um),
                'diameter_y': 4-sigma diameter Y (um),
                'centroid_x': Centroid X position,
                'centroid_y': Centroid Y position,
                'fps': Frame rate (if available)
            }
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        cam = self.sdk.cameras[self.camera_index]
        
        # Try to get FPS, fallback if not available
        try:
            fps = float(cam.fps) if hasattr(cam, 'fps') else 0.0
        except:
            fps = 0.0
        
        return {
            'diameter_x': float(cam.Image.DiameterInfo.diameter4SigmaX),
            'diameter_y': float(cam.Image.DiameterInfo.diameter4SigmaY),
            'centroid_x': float(cam.Image.CentroidInfo.centroidXPos),
            'centroid_y': float(cam.Image.CentroidInfo.centroidYPos),
            'fps': fps
        }
    
    def disconnect(self):
        """Disconnect and cleanup"""
        if self.is_connected:
            try:
                self.stop()
            except:
                pass
            self.sdk.cameras[self.camera_index].Dispose()
            self.is_connected = False
            logger.info("Disconnected")
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.disconnect()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Gentec Beamage 4M IR Camera Control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --exposure=92.19 --gain=1
  python main.py --auto-exposure --frames=10
  python main.py --exposure=100 --gain=2 --frames=5 --output=my_capture.npy
        """
    )
    
    # Exposure settings
    exposure_group = parser.add_mutually_exclusive_group()
    exposure_group.add_argument(
        '--exposure',
        type=float,
        metavar='MS',
        help='Set manual exposure time in milliseconds (0.06-5000)'
    )
    exposure_group.add_argument(
        '--auto-exposure',
        action='store_true',
        help='Enable auto exposure mode'
    )
    
    # Gain setting
    parser.add_argument(
        '--gain',
        type=int,
        metavar='N',
        help='Set camera gain (typically 1-4, check SDK docs)'
    )
    
    # Capture settings
    parser.add_argument(
        '--frames',
        type=int,
        default=5,
        metavar='N',
        help='Number of frames to capture (default: 5)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='beamage_capture.npy',
        metavar='FILE',
        help='Output filename for saved image (default: beamage_capture.npy)'
    )
    
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Skip matplotlib visualization'
    )
    
    parser.add_argument(
        '--serial',
        type=str,
        default='228451',
        metavar='SN',
        help='Camera serial number (default: 228451)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    print("\n" + "="*70)
    print("Gentec Beamage 4M IR Camera - Python Interface")
    print("="*70 + "\n")
    
    # Create camera instance
    cam = BeamageCamera(serial_number=args.serial)
    
    try:
        # Connect
        if not cam.connect():
            print("\n❌ Failed to connect!")
            print("Check:")
            print("  1. Camera is plugged in (USB3)")
            print("  2. Drivers are installed")
            print("  3. PC-BEAMAGE can see the camera")
            print("  4. DLL_PATH is correct in this script")
            exit(1)
        
        print("\n✓ Camera connected!")
        
        # Configure exposure
        print("\n--- Configuring camera ---")
        if args.auto_exposure:
            cam.set_auto_exposure(True)
            print("Auto exposure: ENABLED")
        elif args.exposure is not None:
            cam.set_exposure(args.exposure)
            print(f"Manual exposure: {args.exposure} ms")
        else:
            # Default to auto if neither specified
            cam.set_auto_exposure(True)
            print("Auto exposure: ENABLED (default)")
        
        # Configure gain
        if args.gain is not None:
            cam.set_gain(args.gain)
            print(f"Gain: {args.gain}")
        
        # Show current settings
        current_exp = cam.get_exposure()
        current_gain = cam.get_gain()
        print(f"\nCurrent settings:")
        print(f"  Exposure: {current_exp:.2f} ms")
        if current_gain != -1:
            print(f"  Gain: {current_gain}")
        
        # Start capture
        print("\n--- Starting capture ---")
        cam.start()
        time.sleep(1)  # Let it stabilize
        
        # Capture images
        print(f"\n--- Capturing {args.frames} frames ---")
        for i in range(args.frames):
            img = cam.capture()
            stats = cam.get_beam_stats()
            
            print(f"\nFrame {i+1}/{args.frames}:")
            print(f"  Image shape: {img.shape}")
            print(f"  Min/Max: {img.min()} / {img.max()}")
            print(f"  Beam 4σ: X={stats['diameter_x']:.2f} µm, "
                  f"Y={stats['diameter_y']:.2f} µm")
            print(f"  Centroid: ({stats['centroid_x']:.1f}, "
                  f"{stats['centroid_y']:.1f})")
            print(f"  FPS: {stats['fps']:.1f}")
            
            time.sleep(0.5)
        
        # Save last image
        print(f"\n--- Saving image ---")
        np.save(args.output, img)
        print(f"✓ Saved to {args.output}")
        
        # Optional: plot with matplotlib
        if not args.no_plot:
            try:
                import matplotlib.pyplot as plt
                plot_filename = args.output.replace('.npy', '.png')
                plt.figure(figsize=(8, 8))
                plt.imshow(img, cmap='hot', origin='lower')
                plt.colorbar(label='Intensity')
                plt.title(f"Beamage 4M IR - S/N:{cam.serial_number}\n"
                         f"Exp: {current_exp:.2f}ms, Gain: {current_gain if current_gain != -1 else 'N/A'}")
                plt.xlabel("X (pixels)")
                plt.ylabel("Y (pixels)")
                plt.tight_layout()
                plt.savefig(plot_filename, dpi=150)
                print(f"✓ Saved plot to {plot_filename}")
                # plt.show()  # Uncomment to display
            except ImportError:
                print("(matplotlib not installed, skipping plot)")
        
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        cam.disconnect()
        print("\nCleaned up")