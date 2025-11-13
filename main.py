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

"""

import clr
import sys
import numpy as np
from pathlib import Path
from typing import Optional, Dict
import logging
import time

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
    
    def capture(self) -> np.ndarray:
        """
        Capture single image
        
        Returns:
            np.ndarray: Image as 2D array (2048x2048)
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        # Get raw image buffer
        img_data = self.sdk.cameras[self.camera_index].Image.GetImage()
        width = self.sdk.cameras[self.camera_index].Image.width
        height = self.sdk.cameras[self.camera_index].Image.height
        
        # Convert to numpy (SDK returns 1D array, reshape to 2D)
        img_array = np.array(list(img_data), dtype=np.int32)
        img_2d = img_array.reshape((height, width))
        
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
                'fps': Frame rate
            }
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        cam = self.sdk.cameras[self.camera_index]
        
        return {
            'diameter_x': float(cam.Image.DiameterInfo.diameter4SigmaX),
            'diameter_y': float(cam.Image.DiameterInfo.diameter4SigmaY),
            'centroid_x': float(cam.Image.CentroidInfo.centroidXPos),
            'centroid_y': float(cam.Image.CentroidInfo.centroidYPos),
            'fps': float(cam.cameraFps)
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


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Gentec Beamage 4M IR Camera - Python Interface")
    print("="*70 + "\n")
    
    # Create camera instance
    cam = BeamageCamera(serial_number="228451")
    
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
        
        # Configure
        print("\n--- Configuring camera ---")
        cam.set_auto_exposure(True)  # or cam.set_exposure(100.0)
        print(f"Current exposure: {cam.get_exposure():.2f} ms")
        
        # Start capture
        print("\n--- Starting capture ---")
        cam.start()
        time.sleep(1)  # Let it stabilize
        
        # Capture some images
        print("\n--- Capturing images ---")
        for i in range(5):
            img = cam.capture()
            stats = cam.get_beam_stats()
            
            print(f"\nFrame {i+1}:")
            print(f"  Image shape: {img.shape}")
            print(f"  Min/Max: {img.min()} / {img.max()}")
            print(f"  Beam 4σ: X={stats['diameter_x']:.2f} µm, "
                  f"Y={stats['diameter_y']:.2f} µm")
            print(f"  Centroid: ({stats['centroid_x']:.1f}, "
                  f"{stats['centroid_y']:.1f})")
            print(f"  FPS: {stats['fps']:.1f}")
            
            time.sleep(0.5)
        
        # Save last image
        print("\n--- Saving image ---")
        np.save("beamage_capture.npy", img)
        print("✓ Saved to beamage_capture.npy")
        
        # Optional: plot with matplotlib
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8, 8))
            plt.imshow(img, cmap='hot', origin='lower')
            plt.colorbar(label='Intensity')
            plt.title(f"Beamage 4M IR - S/N:{cam.serial_number}")
            plt.xlabel("X (pixels)")
            plt.ylabel("Y (pixels)")
            plt.tight_layout()
            plt.savefig("beamage_capture.png", dpi=150)
            print("✓ Saved plot to beamage_capture.png")
            # plt.show()  # Uncomment to display
        except ImportError:
            print("(matplotlib not installed, skipping plot)")
        
        print("\n" + "="*70)
        print("✓ Success! You're ready to integrate this into your code")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        cam.disconnect()
        print("\nCleaned up")