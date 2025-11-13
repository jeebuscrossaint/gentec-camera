using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using BeamageApi;

namespace Beamage_SDK_Example
{
   public partial class MainForm : Form
    {
        BSDK bsdk;
		int selectedIndex = 0;
		int topROI = 0;
		int heigthROI = 2048;
		int canvasSize = 2048;
		bool bAutotraking = false;
		bool bShowImage = false;
        bool bGrayscale = false;
		bool bExposureTime = false;
		bool bCropImage = false;
		List<int> connectedCamList = new List<int>();
		List<int> selectedIndexRunList = new List<int>();
		private List<String> cameras                = new List<String>();
        public  bool         capture                = false;
        public bool myVariable = false;

        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            dataGridViewCameras.ColumnCount = 6;
            dataGridViewCameras.Columns[0].Name = "Serial Number";
            dataGridViewCameras.Columns[1].Name = "4 Sigma X";
            dataGridViewCameras.Columns[2].Name = "4 Sigma Y";
            dataGridViewCameras.Columns[3].Name = "Centroid X";
            dataGridViewCameras.Columns[4].Name = "Centroid Y";
            dataGridViewCameras.Columns[5].Name = "FPS";

            labelSelectedItem.Text = $"Cam # : {selectedIndex}";

            textBoxCanvasSize.Text = "2048";

            SetDefautStateButtons(false);

            CreateBsdk();

        }


        #region Functions

        private void RemoveEvent(object sender, EventArgs e)
        {
            // A camera has been disconnected from this PC
        }

        private void AttachedEvent(object sender, EventArgs e)
        {
            // A camera has been connected from this PC
        }

        private void ErrorsEvent(object sender, EventArgs e)
        {
            // Error messages from Error Manager
            string error = ((BErrorsManager)sender).Error;
            MessageBox.Show(error);
        }

        private void CreateBsdk()
        {
            // Create SDK
            bsdk = new BSDK();

            // Assign an event handler for attached and removed device 
            bsdk.AttachedStateChanged   += new EventHandler(AttachedEvent);
            bsdk.RemoveStateChanged     += new EventHandler(RemoveEvent);
            labelSDKVersion.Text        = $"SDK version : {bsdk.GetVersion()}";
        }

        private void SetStateButtons(bool state)
        {
            buttonRunAll.Enabled        = state;
            buttonRun.Enabled           = state;
            buttonStop.Enabled          = state;
            detectCamerasButton.Enabled = state;

        }

        private void SetDefautStateButtons(bool state)
        {
            buttonRun.Enabled       = state;
            buttonRunAll.Enabled    = state;
            buttonStop.Enabled      = state;
            buttonStopAll.Enabled   = state;
        }

        private void SetStateButtonsAllCameras(bool state)
        {
            buttonStopAll.Enabled       = state;
            buttonRunAll.Enabled        = state;
            detectCamerasButton.Enabled = state;
        }

        private void BackgroundIsReady(object sender, EventArgs e)
        {
            MessageBox.Show("Background is Ready", "Background", MessageBoxButtons.OK, MessageBoxIcon.Information);
            bsdk.cameras[selectedIndex].BackgroundIsReadyEvent -= new EventHandler(BackgroundIsReady);
        }

        public bool ThumbnailCallback()
        {
            return false;
        }

        #endregion

        #region Image Functions

        private void NewImageAllCam(object sender, EventArgs e)
        {
            Image.GetThumbnailImageAbort myCallback = new Image.GetThumbnailImageAbort(ThumbnailCallback);

            if (dataGridViewCameras.InvokeRequired)
            {
                dataGridViewCameras.Invoke(new MethodInvoker(delegate
                {
                    int nIndex = 0;
                    foreach (var item in cameras)
                    {
                        dataGridViewCameras.Rows[nIndex].Cells["Serial Number"].Value   = bsdk.cameras[nIndex].Properties.GetSerialNumber();
                        dataGridViewCameras.Rows[nIndex].Cells["4 Sigma X"].Value       = bsdk.cameras[nIndex].Image.DiameterInfo.diameter4SigmaX.ToString("0.00");
                        dataGridViewCameras.Rows[nIndex].Cells["4 Sigma Y"].Value       = bsdk.cameras[nIndex].Image.DiameterInfo.diameter4SigmaY.ToString("0.00");
                        dataGridViewCameras.Rows[nIndex].Cells["Centroid X"].Value      = bsdk.cameras[nIndex].Image.CentroidInfo.centroidXPos.ToString("0.00");
                        dataGridViewCameras.Rows[nIndex].Cells["Centroid Y"].Value      = bsdk.cameras[nIndex].Image.CentroidInfo.centroidYPos.ToString("0.00");
                        dataGridViewCameras.Rows[nIndex].Cells["FPS"].Value             = bsdk.cameras[nIndex].fps.ToString("0.00");

                        nIndex++;
                    }

                }));

                if ((selectedIndex >= 0) && (selectedIndex < bsdk.cameras.Count) && pictureBox.InvokeRequired && bShowImage)
                {
                    pictureBox.Invoke(new MethodInvoker(delegate
                    {
                        Image image         = bsdk.cameras[selectedIndex].Image.GetBmpRealColor();
                        pictureBox.Image    = image.GetThumbnailImage(image.Width / 4, image.Height / 4, myCallback, IntPtr.Zero);
                    }));
                }
                else
                {
                    pictureBox.Image = null;
                }


                if (labelTop.InvokeRequired)
                {
                    labelTop.Invoke(new MethodInvoker(delegate { labelTop.Text = $"Top: ( {topROI}, {heigthROI} )"; }));
                }

                if (labelSize.InvokeRequired)
                {
                    labelSize.Invoke(new MethodInvoker(delegate { labelSize.Text = $"Center (Relative): ({bsdk.cameras[selectedIndex].Image.CenterPosX} ,  { bsdk.cameras[selectedIndex].Image.CenterPosY})"; }));
				}

				if (textBoxExposureTime.InvokeRequired && bExposureTime)
                {
                    textBoxExposureTime.Invoke(new MethodInvoker(delegate { textBoxExposureTime.Text = bsdk.cameras[selectedIndex].Settings.exposureTime.ToString("0.000"); }));
                }

                for (int i = 0; i < bsdk.cameras.Count; i++)
                {
                    if (bAutotraking)
                    {
                        if (bsdk.cameras[i].Image.CenterPosY > heigthROI / 2) topROI += Math.Abs(bsdk.cameras[i].Image.CenterPosY - heigthROI / 2) / 2;
                        else topROI -= Math.Abs(bsdk.cameras[i].Image.CenterPosY - heigthROI / 2) / 2;

                        // Bondaries values
                        if (topROI < 0) topROI = 0;
                        if (topROI > (2048 - heigthROI)) topROI = (2048 - heigthROI);

                        bsdk.cameras[i].SetROI(topROI, heigthROI);
                    }
                }
            }
        }

        #endregion

        #region Buttons Functions

        private void ButtonRun_Click(object sender, EventArgs e)
        {
            int nIndex = 0;

            connectedCamList.Clear();


            foreach (var item in bsdk.cameras)
            {
                bsdk.cameras[nIndex].Connect();
                bsdk.cameras[nIndex].Run();
                bsdk.cameras[nIndex].Resize(heigthROI);
                bsdk.cameras[nIndex].SetROI(topROI, heigthROI);
                connectedCamList.Add(nIndex);

                Thread.Sleep(200);

                nIndex++;
            }

            SetStateButtons(false);
            textBoxExposureTime.Text         = bsdk.cameras[selectedIndex].Settings.exposureTime.ToString("0.000");
            bsdk.cameras[0].NewImageEvent   += new EventHandler(NewImageAllCam);
        }

        private void ButtonStop_Click(object sender, EventArgs e)
        {
            int cam = 0;
            foreach (var item in cameras)
            {
                bsdk.cameras[cam].Stop();
                Thread.Sleep(50);
                cam++;
            }
            SetStateButtons(true);
        }

        private void ButtonCamStop_Click(object sender, EventArgs e)
        {
            if (selectedIndex != -1)
            {
                bsdk.cameras[selectedIndex].Stop();
                selectedIndexRunList.Remove(selectedIndex);
            }
            if (selectedIndexRunList.Count == 0)
            {
                SetStateButtonsAllCameras(true);
            }

        }

        private void ButtonCamRun_Click(object sender, EventArgs e)
        {
            if (selectedIndex != -1 && !selectedIndexRunList.Contains(selectedIndex))
            {
                if (connectedCamList.Contains(selectedIndex))
                {
                    bsdk.cameras[selectedIndex].Run();
                    bsdk.cameras[selectedIndex].Resize(heigthROI);
                    bsdk.cameras[selectedIndex].SetROI(topROI, heigthROI);
                }
                else
                {
                    bsdk.cameras[selectedIndex].Connect();
                    bsdk.cameras[selectedIndex].Run();
                    bsdk.cameras[selectedIndex].Resize(heigthROI);
                    bsdk.cameras[selectedIndex].SetROI(topROI, heigthROI);
                    connectedCamList.Add(selectedIndex);
                }

                bsdk.cameras[selectedIndex].NewImageEvent += new EventHandler(NewImageAllCam);
                textBoxExposureTime.Text = bsdk.cameras[selectedIndex].Settings.exposureTime.ToString("0.000");
                selectedIndexRunList.Add(selectedIndex);

                SetStateButtonsAllCameras(false);
            }
        }

        private void DectectCamerasButton_Click(object sender, EventArgs e)
        {
            try
            {
                bsdk.SetCanvas(heigthROI);
                bsdk.Detect();
            }
            catch (Exception exception)
            {
               Debug.WriteLine(exception.ToString());
            }

            cameras.Clear();
            dataGridViewCameras.Rows.Clear();

            foreach (var item in bsdk.cameras)
            {
                cameras.Add(item.Properties.GetSerialNumber());
                dataGridViewCameras.Rows.Add(item.Properties.GetSerialNumber(), "", "", "");
            }

            if (cameras.Count >= 1)
                SetDefautStateButtons(true);
            else
                MessageBox.Show("No camera has been detected", "Detection Cameras", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        private void ButtonBackground_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Please Block your laser", "BackGround", MessageBoxButtons.OK, MessageBoxIcon.Information);
            checkBoxExposureTime.Checked = false;
            checkBoxAutoTracking.Checked = false;

            bsdk.cameras[selectedIndex].SetToAutoExposure(false);
            bsdk.cameras[selectedIndex].RunBackground();
            while (!bsdk.cameras[selectedIndex].bBackgroundDone) { Thread.Sleep(100); }

            MessageBox.Show("Background is Ready", "Background", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void ButtonSaveBackground_Click(object sender, EventArgs e)
        {
            //Save background file
            SaveFileDialog saveDialog = new SaveFileDialog();
            saveDialog.Title = "Save Background";
            saveDialog.Filter = "sdk files (*.csv)|*.csv|All files (*.*)|*.*";
            saveDialog.FileName = $"{bsdk.cameras[selectedIndex].Properties.GetSerialNumber()}_";

            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                bsdk.cameras[selectedIndex].SaveBackGround(saveDialog.FileName);
                MessageBox.Show("The background has been saved!", "Save Background", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void ButtonLoadBackground_Click(object sender, EventArgs e)
        {
            //Open Background File
            OpenFileDialog loadDialog = new OpenFileDialog();
            loadDialog.Title = "Open Background File";
            loadDialog.Filter = "csv files|*.csv";

            if (loadDialog.ShowDialog() == DialogResult.OK)
            {
                bsdk.cameras[selectedIndex].LoadBackGround(loadDialog.FileName);
                MessageBox.Show("The Background has been loaded!", "Load Background", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

        }

        private void ButtonClearBackGround_Click(object sender, EventArgs e)
        {
            bsdk.cameras[selectedIndex].ClearBackGround();
            MessageBox.Show("The Background has been cleared!", "Clear Background", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }


        #endregion

        #region CheckBox Functions

        private void CheckBoxAutoTracking_CheckedChanged(object sender, EventArgs e)
        {
            bAutotraking = !bAutotraking;
        }

        private void CheckBoxShowImage_CheckedChanged(object sender, EventArgs e)
        {
            bShowImage = !bShowImage;
        }

        private void CheckBoxExposureTime_CheckedChanged(object sender, EventArgs e)
        {
            bExposureTime               = !bExposureTime;
            textBoxExposureTime.Enabled = !bExposureTime;
            int cam = 0;
            foreach (var item in cameras)
            {
                bsdk.cameras[cam].SetToAutoExposure(bExposureTime);
                Thread.Sleep(50);
                cam++;
            }
        }

        private void CheckBoxCropImage_CheckedChanged(object sender, EventArgs e)
        {
            bCropImage = !bCropImage;
            bsdk.cameras[selectedIndex].Crop(bCropImage);
        }

        #endregion

        #region DataGrid Functions

        private void DataGridViewCameras_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            selectedIndex = dataGridViewCameras.CurrentCell.RowIndex;
            labelSelectedItem.Text = "Cam # : " + selectedIndex.ToString();
        }

        #endregion

        #region TextBox Functions
        private void TextBoxExposureTime_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!bExposureTime && e.KeyChar == (char)Keys.Enter)
            {
                try
                {
                    bsdk.cameras[selectedIndex].SetExposureTime(float.Parse(textBoxExposureTime.Text, CultureInfo.InvariantCulture.NumberFormat));
                }
                catch (Exception)
                {
                    MessageBox.Show("Please, verify the input data!", "Exposure Time Values", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }

            }
        }

        private void TextBoxCanvasSize_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)Keys.Enter)
            {
                try
                {
                    canvasSize = Convert.ToInt32(textBoxCanvasSize.Text);

                    if (canvasSize < 0 || canvasSize > 2048)
                    {
                        MessageBox.Show("The allows canvas values must be 0 to 2048.", "Canvas Size Values", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        canvasSize = 0;

                    }
                    else
                    {
                        heigthROI = canvasSize;
                        bsdk.cameras[selectedIndex].Resize(heigthROI);
                        Size size = new Size(2048 / 4, heigthROI / 4);
                        pictureBox.Size = size;
                        pictureBox.Update();

                    }
                }
                catch (Exception)
                {
                    MessageBox.Show("Please, verify the input data!", "Canvas Size Values", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
        #endregion

		private void checkBoxGrayScale_CheckedChanged(object sender, EventArgs e)
		{
			bGrayscale = !bGrayscale;
			bsdk.cameras[selectedIndex].GrayScale(bGrayscale);
		}
	}
}
