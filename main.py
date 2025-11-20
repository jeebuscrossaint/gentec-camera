"""
Gentec Beamage 4M IR Camera - Python Interface
CLI tool for capturing beam profile images

Requirements:
    pip install pythonnet numpy matplotlib astropy

Usage:
    python main.py --help
    python main.py --auto-exposure --frames 10
    python main.py --exposure 50.5 --output my_capture.fits
"""

import clr
import sys
import argparse
import numpy as np
from pathlib import Path
from typing import Optional, Dict
import logging
import time
import threading

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Find DLL relative to script
SCRIPT_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd()
DEFAULT_DLL_PATH = SCRIPT_DIR / "Example_Beamage_SDK_CSharp_V1.02.02" / "3. DLL File" / "BeamageSDK.dll"


class BeamageCamera:
    """Python wrapper for Gentec Beamage 4M IR camera"""
    
    def __init__(self, dll_path: Path, serial_number: Optional[str] = None):
        self.serial_number = serial_number
        self.camera_index = None
        self.is_connected = False
        
        # Image buffer updated by event
        self._latest_image = None
        self._image_ready = threading.Event()
        self._image_lock = threading.Lock()
        
        # Load DLL
        if not dll_path.exists():
            raise FileNotFoundError(f"BeamageSDK.dll not found at {dll_path}")
        
        sys.path.append(str(dll_path.parent))
        clr.AddReference(str(dll_path.stem))
        
        from BeamageApi import BSDK
        self.sdk = BSDK()
        
        # Set canvas to full sensor size BEFORE detecting
        self.sdk.SetCanvas(2048)
        
        logger.info(f"SDK initialized (version: {self.sdk.GetVersion()})")
    
    def _on_new_image(self, sender, event_args):
        """Event handler called when a new image is captured"""
        try:
            cam = self.sdk.cameras[self.camera_index]
            img_data = cam.Image.GetImage()
            
            # Convert to numpy
            img_array = np.array(list(img_data), dtype=np.int32)
            
            # Get dimensions from SDK
            width = cam.Image.width
            height = cam.Image.height
            
            # Reshape
            if len(img_array) == width * height:
                img_2d = img_array.reshape((height, width))
            else:
                # Fallback to full sensor
                total = len(img_array)
                h = total // 2048
                img_2d = img_array.reshape((h, 2048))
            
            with self._image_lock:
                self._latest_image = img_2d.copy()
            
            self._image_ready.set()
            
        except Exception as e:
            logger.error(f"Error in image callback: {e}")
    
    def connect(self, camera_index: int = 0) -> bool:
        """Detect and connect to camera"""
        try:
            self.sdk.Detect()
            
            if self.sdk.cameras.Count == 0:
                logger.error("No cameras detected! Check USB connection.")
                return False
            
            logger.info(f"Found {self.sdk.cameras.Count} camera(s)")
            
            # List cameras
            for i in range(self.sdk.cameras.Count):
                serial = self.sdk.cameras[i].Properties.GetSerialNumber()
                is_4m = self.sdk.cameras[i].Properties.Is4mSensor()
                model = "Beamage-4M" if is_4m else "Beamage-3.0"
                logger.info(f"  [{i}] {model} S/N:{serial}")
            
            # Find camera by serial if specified
            if self.serial_number:
                found = False
                for i in range(self.sdk.cameras.Count):
                    if self.sdk.cameras[i].Properties.GetSerialNumber() == self.serial_number:
                        camera_index = i
                        found = True
                        break
                if not found:
                    logger.error(f"Camera with S/N {self.serial_number} not found")
                    return False
            
            if camera_index >= self.sdk.cameras.Count:
                logger.error(f"Camera index {camera_index} out of range")
                return False
            
            self.camera_index = camera_index
            cam = self.sdk.cameras[self.camera_index]
            
            # Connect to camera
            cam.Connect()
            
            # Set full sensor ROI (important!)
            cam.Resize(2048)
            cam.SetROI(0, 2048)  # top=0, height=2048 (full sensor)
            
            # Subscribe to new image event
            cam.NewImageEvent += self._on_new_image
            
            self.is_connected = True
            
            serial = cam.Properties.GetSerialNumber()
            logger.info(f"Connected to camera {camera_index} (S/N:{serial})")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self):
        """Start continuous capture"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        self.sdk.cameras[self.camera_index].Run()
        logger.info("Started capture")
    
    def stop(self):
        """Stop capture"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        self.sdk.cameras[self.camera_index].StopRun()
        logger.info("Stopped capture")
    
    def set_exposure(self, time_ms: float):
        """Set manual exposure time (0.06-5000 ms)"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        if not (0.06 <= time_ms <= 5000):
            raise ValueError("Exposure must be 0.06-5000 ms")
        
        self.sdk.cameras[self.camera_index].SetToAutoExposure(False)
        self.sdk.cameras[self.camera_index].SetExposureTime(float(time_ms))
        logger.info(f"Set exposure: {time_ms} ms (manual)")
    
    def set_auto_exposure(self, enable: bool = True):
        """Enable/disable auto exposure"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        self.sdk.cameras[self.camera_index].SetToAutoExposure(enable)
        logger.info(f"Auto exposure: {'ON' if enable else 'OFF'}")
    
    def get_exposure(self) -> float:
        """Get current exposure time in ms"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        return float(self.sdk.cameras[self.camera_index].Settings.exposureTime)
    
    def capture(self, timeout: float = 5.0) -> np.ndarray:
        """
        Capture a fresh image using the event system
        
        Args:
            timeout: Max seconds to wait for new frame
        
        Returns:
            2D numpy array of image data
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        # Clear the event flag
        self._image_ready.clear()
        
        # Wait for new image event
        if not self._image_ready.wait(timeout=timeout):
            raise TimeoutError(f"No image received within {timeout} seconds")
        
        # Get the image
        with self._image_lock:
            if self._latest_image is None:
                raise RuntimeError("Image buffer is empty")
            return self._latest_image.copy()
    
    def grab_single_frame(self, timeout: float = 5.0) -> np.ndarray:
        """
        Grab exactly one frame (stops after capture)
        """
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        self._image_ready.clear()
        self.sdk.cameras[self.camera_index].GrabOneFrame()
        
        if not self._image_ready.wait(timeout=timeout):
            raise TimeoutError(f"No image received within {timeout} seconds")
        
        with self._image_lock:
            return self._latest_image.copy()
    
    def get_beam_stats(self) -> Dict:
        """Get beam analysis parameters"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        cam = self.sdk.cameras[self.camera_index]
        
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
                cam = self.sdk.cameras[self.camera_index]
                cam.NewImageEvent -= self._on_new_image
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


def save_fits(filepath: Path, data: np.ndarray, stats: Dict, 
              exposure_ms: float, serial: str, n_frames: int):
    """Save image data to FITS file with proper headers"""
    try:
        from astropy.io import fits
        from datetime import datetime, timezone
    except ImportError:
        logger.error("astropy not installed! Run: pip install astropy")
        raise
    
    hdu = fits.PrimaryHDU(data)
    header = hdu.header
    
    header['SIMPLE'] = True
    header['BITPIX'] = 32
    header['NAXIS'] = len(data.shape)
    
    header['DATE-OBS'] = datetime.now(timezone.utc).isoformat()
    header['TELESCOP'] = 'CREOL Astrophotonics Lab'
    header['INSTRUME'] = 'Gentec Beamage 4M IR'
    header['SERIAL'] = serial
    header['DETECTOR'] = 'Beamage-4M'
    header['NAXIS1'] = data.shape[-1]
    header['NAXIS2'] = data.shape[-2] if len(data.shape) >= 2 else 1
    if len(data.shape) == 3:
        header['NAXIS3'] = data.shape[0]
    header['PIXSIZE'] = (5.5, 'Pixel size in micrometers')
    header['PIXSZ_X'] = (5.5, '[um] Pixel size X')
    header['PIXSZ_Y'] = (5.5, '[um] Pixel size Y')
    header['EXPTIME'] = (exposure_ms / 1000.0, '[s] Exposure time')
    header['EXPOSURE'] = (exposure_ms, '[ms] Exposure time')
    header['BEAM_DX'] = (stats['diameter_x'], '[um] Beam diameter 4-sigma X')
    header['BEAM_DY'] = (stats['diameter_y'], '[um] Beam diameter 4-sigma Y')
    header['CENTX'] = (stats['centroid_x'], '[pix] Centroid X position')
    header['CENTY'] = (stats['centroid_y'], '[pix] Centroid Y position')
    header['DATAMIN'] = int(data.min())
    header['DATAMAX'] = int(data.max())
    header['DATAMEAN'] = float(data.mean())
    header['DATASTD'] = float(data.std())
    header['NFRAMES'] = (n_frames, 'Number of frames')
    header['WAVELEN'] = (1550, '[nm] Nominal wavelength')
    header['WAVEMIN'] = (1495, '[nm] Minimum wavelength')
    header['WAVEMAX'] = (1595, '[nm] Maximum wavelength')
    header['SOFTWARE'] = 'beamage-capture'
    header['SDKVER'] = '1.2.0.2'
    header['COMMENT'] = 'Captured with Gentec Beamage 4M IR camera'
    header['COMMENT'] = 'CREOL - UCF Astrophotonics Lab'
    header['COMMENT'] = 'Dr. Eikenberry Research Group'
    header['HISTORY'] = f'Captured {n_frames} frame(s)'
    header['HISTORY'] = f'Exposure: {exposure_ms} ms'
    
    hdu.writeto(filepath, overwrite=True)
    print(f"Saved FITS to {filepath}")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Gentec Beamage 4M IR Camera - Capture Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --auto-exposure --frames 10
    %(prog)s --exposure 50.5 --output my_capture.fits
    %(prog)s --exposure 100 --frames 1 --no-plot
    %(prog)s --serial 228451 --auto-exposure
        """
    )
    
    exp_group = parser.add_mutually_exclusive_group()
    exp_group.add_argument('--exposure', type=float, metavar='MS',
        help='Set manual exposure time in milliseconds (0.06-5000)')
    exp_group.add_argument('--auto-exposure', action='store_true',
        help='Enable auto exposure mode')
    
    parser.add_argument('--gain', type=float, metavar='N',
        help='Set camera gain (if supported by SDK)')
    parser.add_argument('--frames', type=int, default=5, metavar='N',
        help='Number of frames to capture (default: 5)')
    parser.add_argument('--delay', type=float, default=0.5, metavar='SEC',
        help='Delay between frames in seconds (default: 0.5)')
    parser.add_argument('--output', type=str, default='beamage_capture.fits', metavar='FILE',
        help='Output filename (.fits, .npy, or .png) (default: beamage_capture.fits)')
    parser.add_argument('--no-plot', action='store_true',
        help='Skip matplotlib visualization')
    parser.add_argument('--save-all', action='store_true',
        help='Save all frames, not just the last one')
    parser.add_argument('--serial', type=str, metavar='SN',
        help='Camera serial number (default: first detected)')
    parser.add_argument('--dll', type=str, metavar='PATH',
        help=f'Path to BeamageSDK.dll (default: {DEFAULT_DLL_PATH})')
    parser.add_argument('--quiet', '-q', action='store_true',
        help='Suppress info messages')
    parser.add_argument('--verbose', '-v', action='store_true',
        help='Enable debug messages')
    parser.add_argument('--timeout', type=float, default=5.0, metavar='SEC',
        help='Timeout for frame capture in seconds (default: 5.0)')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    dll_path = Path(args.dll) if args.dll else DEFAULT_DLL_PATH
    
    print("\n" + "="*60)
    print("Gentec Beamage 4M IR Camera")
    print("="*60 + "\n")
    
    try:
        cam = BeamageCamera(dll_path=dll_path, serial_number=args.serial)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1
    
    try:
        if not cam.connect():
            return 1
        
        # Configure exposure
        if args.auto_exposure:
            cam.set_auto_exposure(True)
        elif args.exposure is not None:
            cam.set_exposure(args.exposure)
        else:
            cam.set_auto_exposure(True)
        
        if args.gain is not None:
            logger.warning("Gain setting not supported by this SDK version")
        
        print(f"Current exposure: {cam.get_exposure():.2f} ms")
        
        # Start capture
        cam.start()
        
        # Wait for camera to stabilize and start sending frames
        print("Waiting for camera to stabilize...")
        time.sleep(2)
        
        # Capture frames
        print(f"\nCapturing {args.frames} frame(s)...\n")
        
        images = []
        stats = None
        
        for i in range(args.frames):
            try:
                img = cam.capture(timeout=args.timeout)
                stats = cam.get_beam_stats()
                images.append(img)
                
                print(f"Frame {i+1}/{args.frames}:")
                print(f"  Shape: {img.shape}")
                print(f"  Min: {img.min()}, Max: {img.max()}, Mean: {img.mean():.2f}")
                print(f"  Beam 4σ: X={stats['diameter_x']:.2f} µm, Y={stats['diameter_y']:.2f} µm")
                print(f"  Centroid: ({stats['centroid_x']:.1f}, {stats['centroid_y']:.1f})")
                print()
                
            except TimeoutError as e:
                logger.error(f"Frame {i+1}: {e}")
                continue
            
            if i < args.frames - 1:
                time.sleep(args.delay)
        
        if not images:
            logger.error("No images captured!")
            return 1
        
        # Save output
        output_path = Path(args.output)
        ext = output_path.suffix.lower()
        
        if args.save_all:
            save_data = np.stack(images, axis=0)
            n_frames = len(images)
        else:
            save_data = images[-1]
            n_frames = 1
        
        serial = args.serial or cam.sdk.cameras[cam.camera_index].Properties.GetSerialNumber()
        
        if ext == '.fits':
            save_fits(output_path, save_data, stats, cam.get_exposure(), serial, n_frames)
        elif ext == '.npy':
            np.save(output_path, save_data)
            print(f"Saved to {output_path}")
        else:
            output_path = output_path.with_suffix('.fits')
            save_fits(output_path, save_data, stats, cam.get_exposure(), serial, n_frames)
        
        # Plot
        if not args.no_plot:
            try:
                import matplotlib.pyplot as plt
                
                img = images[-1]
                
                fig, axes = plt.subplots(1, 2, figsize=(14, 6))
                
                # Full image with better scaling
                vmin, vmax = np.percentile(img, [1, 99.9])
                im0 = axes[0].imshow(img, cmap='hot', origin='lower', vmin=vmin, vmax=vmax)
                axes[0].set_title(f"Full Sensor ({img.shape[1]}×{img.shape[0]})")
                axes[0].set_xlabel("X (pixels)")
                axes[0].set_ylabel("Y (pixels)")
                plt.colorbar(im0, ax=axes[0], label='Intensity')
                
                # Find actual peak location
                y_peak, x_peak = np.unravel_index(img.argmax(), img.shape)
                
                # Zoomed view around actual peak
                zoom = 50
                x_min = max(0, x_peak - zoom)
                x_max = min(img.shape[1], x_peak + zoom)
                y_min = max(0, y_peak - zoom)
                y_max = min(img.shape[0], y_peak + zoom)
                
                zoomed = img[y_min:y_max, x_min:x_max]
                
                im1 = axes[1].imshow(zoomed, cmap='hot', origin='lower',
                                     extent=[x_min, x_max, y_min, y_max])
                axes[1].set_title(f"Zoomed around peak ({x_peak}, {y_peak})")
                axes[1].set_xlabel("X (pixels)")
                axes[1].set_ylabel("Y (pixels)")
                axes[1].axhline(y=y_peak, color='cyan', linestyle='--', alpha=0.5)
                axes[1].axvline(x=x_peak, color='cyan', linestyle='--', alpha=0.5)
                plt.colorbar(im1, ax=axes[1], label='Intensity')
                
                plt.suptitle(f"Beamage 4M IR - S/N:{serial}")
                plt.tight_layout()
                
                plot_path = output_path.with_suffix('.png')
                plt.savefig(plot_path, dpi=150)
                print(f"Saved plot to {plot_path}")
                
                plt.show()
                
            except ImportError:
                logger.warning("matplotlib not installed, skipping plot")
        
        print("\nDone!")
        return 0
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
        
    finally:
        cam.disconnect()


if __name__ == "__main__":
    sys.exit(main())