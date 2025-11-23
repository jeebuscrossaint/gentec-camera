# gentec-camera
please let me get on a paper 
TL;DR Windows Setup:

Install PC-BEAMAGE software + drivers (from Gentec website)
Test camera works in the PC-BEAMAGE GUI
Download the SDK (from that email link)
Install pythonnet: pip install pythonnet numpy matplotlib
Update DLL_PATH in my script to point to BeamageSDK.dll
Run it!

The script I just made:

✅ Simple API: connect(), set_exposure(), capture()
✅ Returns numpy arrays directly
✅ Includes beam analysis (4-sigma diameter, centroid, FPS)
✅ Has a working example at the bottom
✅ Auto-saves images and plots

Just change line 34 where it says DLL_PATH = r"C:\Path\To\BeamageSDK.dll" to wherever you extract the SDK, and you're golden.
The example at the bottom will capture 5 frames, print stats, save the data as .npy, and even generate a matplotlib plot if you have it installed.


NOTE for some reason on my goofy laptop i gotta enter powershell then run cmd then run pwsh then run conda activate gentec-camera
i love conda
please numpy just update to python 3.14 already bro its been a month

note please do run this twin
unblock-File -Path ".\Example_Beamage_SDK_CSharp_V1.02.02\3. DLL File\BeamageSDK.dll"

the above freaky powershell command simply lets windows run the code with teh dll since by the default windows doesnt let you just mess around with remotely downloaded dlls

(can a man just use shared objects?)
