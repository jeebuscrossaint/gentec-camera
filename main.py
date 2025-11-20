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
        
        # Load DLL
        if not dll_path.exists():
            raise FileNotFoundError(f"BeamageSDK.dll not found at {dll_path}")
        
        sys.path.append(str(dll_path.parent))
        clr.AddReference(str(dll_path.stem))
        
        from BeamageApi import BSDK
        self.sdk = BSDK()
        
        logger.info(f"SDK initialized (version: {self.sdk.GetVersion()})")
    
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
            self.sdk.cameras[self.camera_index].Connect()
            self.is_connected = True
            
            serial = self.sdk.cameras[self.camera_index].Properties.GetSerialNumber()
            logger.info(f"Connected to camera {camera_index} (S/N:{serial})")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
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
    
    def capture(self) -> np.ndarray:
        """Capture single image, returns 2D numpy array"""
        if not self.is_connected:
            raise RuntimeError("Not connected!")
        
        img_data = self.sdk.cameras[self.camera_index].Image.GetImage()
        img_array = np.array(list(img_data), dtype=np.int32)
        
        # Reshape to actual dimensions
        total_pixels = len(img_array)
        width = 2048
        height = total_pixels // width
        
        return img_array.reshape((height, width))
    
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
    """
    Save image data to FITS file with proper headers
    
    Args:
        filepath: Output path
        data: Image data (2D or 3D array)
        stats: Beam statistics dict
        exposure_ms: Exposure time in milliseconds
        serial: Camera serial number
        n_frames: Number of frames
    """
    try:
        from astropy.io import fits
        from datetime import datetime, timezone
    except ImportError:
        logger.error("astropy not installed! Run: pip install astropy")
        raise
    
    # Create primary HDU with image data
    hdu = fits.PrimaryHDU(data)
    header = hdu.header
    
    # Standard FITS keywords
    header['SIMPLE'] = True
    header['BITPIX'] = 32  # 32-bit integer
    header['NAXIS'] = len(data.shape)
    
    # Observation info
    header['DATE-OBS'] = datetime.now(timezone.utc).isoformat()
    header['TELESCOP'] = 'CREOL Astrophotonics Lab'
    header['INSTRUME'] = 'Gentec Beamage 4M IR'
    header['SERIAL'] = serial
    
    # Detector info
    header['DETECTOR'] = 'Beamage-4M'
    header['NAXIS1'] = data.shape[-1]  # Width
    header['NAXIS2'] = data.shape[-2] if len(data.shape) >= 2 else 1  # Height
    if len(data.shape) == 3:
        header['NAXIS3'] = data.shape[0]  # Number of frames
    header['PIXSIZE'] = (5.5, 'Pixel size in micrometers')
    header['PIXSZ_X'] = (5.5, '[um] Pixel size X')
    header['PIXSZ_Y'] = (5.5, '[um] Pixel size Y')
    
    # Exposure info
    header['EXPTIME'] = (exposure_ms / 1000.0, '[s] Exposure time')
    header['EXPOSURE'] = (exposure_ms, '[ms] Exposure time')
    
    # Beam parameters
    header['BEAM_DX'] = (stats['diameter_x'], '[um] Beam diameter 4-sigma X')
    header['BEAM_DY'] = (stats['diameter_y'], '[um] Beam diameter 4-sigma Y')
    header['CENTX'] = (stats['centroid_x'], '[pix] Centroid X position')
    header['CENTY'] = (stats['centroid_y'], '[pix] Centroid Y position')
    
    # Data statistics
    header['DATAMIN'] = int(data.min())
    header['DATAMAX'] = int(data.max())
    header['DATAMEAN'] = float(data.mean())
    header['DATASTD'] = float(data.std())
    
    # Frame info
    header['NFRAMES'] = (n_frames, 'Number of frames')
    
    # Wavelength (Beamage 4M IR range)
    header['WAVELEN'] = (1550, '[nm] Nominal wavelength')
    header['WAVEMIN'] = (1495, '[nm] Minimum wavelength')
    header['WAVEMAX'] = (1595, '[nm] Maximum wavelength')
    
    # Software info
    header['SOFTWARE'] = 'beamage-capture'
    header['SDKVER'] = '1.2.0.2'
    
    # Comments
    header['COMMENT'] = 'Captured with Gentec Beamage 4M IR camera'
    header['COMMENT'] = 'CREOL - UCF Astrophotonics Lab'
    header['COMMENT'] = 'Dr. Eikenberry Research Group'
    
    # History
    header['HISTORY'] = f'Captured {n_frames} frame(s)'
    header['HISTORY'] = f'Exposure: {exposure_ms} ms'
    
    # Write to file
    hdu.writeto(filepath, overwrite=True)
    print(f"Saved FITS to {filepath}")
    print(f"  Headers include: beam stats, exposure, detector info")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Gentec Beamage 4M IR Camera - Capture Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --auto-exposure --frames 10
    %(prog)s --exposure 50.5 --output my_capture.npy
    %(prog)s --exposure 100 --frames 1 --no-plot
    %(prog)s --serial 228451 --auto-exposure
        """
    )
    
    # Exposure settings (mutually exclusive)
    exp_group = parser.add_mutually_exclusive_group()
    exp_group.add_argument(
        '--exposure', 
        type=float, 
        metavar='MS',
        help='Set manual exposure time in milliseconds (0.06-5000)'
    )
    exp_group.add_argument(
        '--auto-exposure', 
        action='store_true',
        help='Enable auto exposure mode'
    )
    
    # Other camera settings
    parser.add_argument(
        '--gain', 
        type=float, 
        metavar='N',
        help='Set camera gain (if supported by SDK)'
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
        '--delay', 
        type=float, 
        default=0.5, 
        metavar='SEC',
        help='Delay between frames in seconds (default: 0.5)'
    )
    
    # Output settings
    parser.add_argument(
        '--output', 
        type=str, 
        default='beamage_capture.fits', 
        metavar='FILE',
        help='Output filename (.fits, .npy, or .png) (default: beamage_capture.fits)'
    )
    parser.add_argument(
        '--no-plot', 
        action='store_true',
        help='Skip matplotlib visualization'
    )
    parser.add_argument(
        '--save-all', 
        action='store_true',
        help='Save all frames, not just the last one'
    )
    
    # Camera selection
    parser.add_argument(
        '--serial', 
        type=str, 
        metavar='SN',
        help='Camera serial number (default: first detected)'
    )
    parser.add_argument(
        '--dll', 
        type=str, 
        metavar='PATH',
        help=f'Path to BeamageSDK.dll (default: {DEFAULT_DLL_PATH})'
    )
    
    # Verbosity
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress info messages'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable debug messages'
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Resolve DLL path
    dll_path = Path(args.dll) if args.dll else DEFAULT_DLL_PATH
    
    print("\n" + "="*60)
    print("Gentec Beamage 4M IR Camera")
    print("="*60 + "\n")
    
    # Create camera instance
    try:
        cam = BeamageCamera(dll_path=dll_path, serial_number=args.serial)
    except FileNotFoundError as e:
        logger.error(str(e))
        logger.error("Please specify --dll path or place SDK in expected location")
        return 1
    
    try:
        # Connect
        if not cam.connect():
            return 1
        
        # Configure exposure
        if args.auto_exposure:
            cam.set_auto_exposure(True)
        elif args.exposure is not None:
            cam.set_exposure(args.exposure)
        else:
            # Default to auto exposure if nothing specified
            cam.set_auto_exposure(True)
        
        # Note: Gain not supported in this SDK version
        if args.gain is not None:
            logger.warning("Gain setting not supported by this SDK version")
        
        print(f"Current exposure: {cam.get_exposure():.2f} ms")
        
        # Start capture
        cam.start()
        time.sleep(1)  # Let camera stabilize
        
        # Capture frames
        print(f"\nCapturing {args.frames} frame(s)...\n")
        
        images = []
        for i in range(args.frames):
            img = cam.capture()
            stats = cam.get_beam_stats()
            images.append(img)
            
            print(f"Frame {i+1}/{args.frames}:")
            print(f"  Shape: {img.shape}, Min/Max: {img.min()}/{img.max()}")
            print(f"  Beam 4σ: X={stats['diameter_x']:.2f} µm, Y={stats['diameter_y']:.2f} µm")
            print(f"  Centroid: ({stats['centroid_x']:.1f}, {stats['centroid_y']:.1f})")
            if stats['fps'] > 0:
                print(f"  FPS: {stats['fps']:.1f}")
            print()
            
            if i < args.frames - 1:
                time.sleep(args.delay)
        
        # Save output
        output_path = Path(args.output)
        ext = output_path.suffix.lower()
        
        # Prepare data to save
        if args.save_all:
            save_data = np.stack(images, axis=0)
            n_frames = len(images)
        else:
            save_data = images[-1]
            n_frames = 1
        
        # Save based on file extension
        if ext == '.fits':
            save_fits(
                output_path, 
                save_data, 
                stats=stats,
                exposure_ms=cam.get_exposure(),
                serial=args.serial or cam.sdk.cameras[cam.camera_index].Properties.GetSerialNumber(),
                n_frames=n_frames
            )
        elif ext == '.npy':
            np.save(output_path, save_data)
            print(f"Saved to {output_path}")
        else:
            # Default to FITS if unknown extension
            output_path = output_path.with_suffix('.fits')
            save_fits(
                output_path, 
                save_data, 
                stats=stats,
                exposure_ms=cam.get_exposure(),
                serial=args.serial or cam.sdk.cameras[cam.camera_index].Properties.GetSerialNumber(),
                n_frames=n_frames
            )
        
        # Plot unless disabled
        if not args.no_plot:
            try:
                import matplotlib.pyplot as plt
                
                img = images[-1]
                
                fig, axes = plt.subplots(1, 2, figsize=(14, 6))
                
                # Full image
                im0 = axes[0].imshow(img, cmap='hot', origin='lower')
                axes[0].set_title(f"Full Sensor (2048×2048)")
                axes[0].set_xlabel("X (pixels)")
                axes[0].set_ylabel("Y (pixels)")
                plt.colorbar(im0, ax=axes[0], label='Intensity')
                
                # Zoomed view around centroid
                cx = int(stats['centroid_x'])
                cy = int(stats['centroid_y'])
                zoom = 50  # pixels around centroid
                
                x_min = max(0, cx - zoom)
                x_max = min(img.shape[1], cx + zoom)
                y_min = max(0, cy - zoom)
                y_max = min(img.shape[0], cy + zoom)
                
                zoomed = img[y_min:y_max, x_min:x_max]
                
                im1 = axes[1].imshow(zoomed, cmap='hot', origin='lower',
                                     extent=[x_min, x_max, y_min, y_max])
                axes[1].set_title(f"Zoomed ({zoom*2}×{zoom*2} around centroid)")
                axes[1].set_xlabel("X (pixels)")
                axes[1].set_ylabel("Y (pixels)")
                plt.colorbar(im1, ax=axes[1], label='Intensity')
                
                plt.suptitle(f"Beamage 4M IR - S/N:{args.serial or 'detected'}")
                plt.tight_layout()
                
                # Save plot
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