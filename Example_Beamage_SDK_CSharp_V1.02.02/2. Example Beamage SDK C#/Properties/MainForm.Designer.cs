namespace Beamage_SDK_Example
{
   partial class MainForm
   {
      /// <summary>
      /// Required designer variable.
      /// </summary>
      private System.ComponentModel.IContainer components = null;

      /// <summary>
      /// Clean up any resources being used.
      /// </summary>
      /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
      protected override void Dispose(bool disposing)
      {
         if (disposing && (components != null))
         {
            components.Dispose();
         }
         base.Dispose(disposing);
      }

      #region Windows Form Designer generated code

      /// <summary>
      /// Required method for Designer support - do not modify
      /// the contents of this method with the code editor.
      /// </summary>
      private void InitializeComponent()
      {
         this.buttonRunAll = new System.Windows.Forms.Button();
         this.buttonStopAll = new System.Windows.Forms.Button();
         this.dataGridViewCameras = new System.Windows.Forms.DataGridView();
         this.buttonRun = new System.Windows.Forms.Button();
         this.buttonStop = new System.Windows.Forms.Button();
         this.labelSelectedItem = new System.Windows.Forms.Label();
         this.pictureBox = new System.Windows.Forms.PictureBox();
         this.detectCamerasButton = new System.Windows.Forms.Button();
         this.checkBoxAutoTracking = new System.Windows.Forms.CheckBox();
         this.labelTop = new System.Windows.Forms.Label();
         this.checkBoxShowImage = new System.Windows.Forms.CheckBox();
         this.labelSize = new System.Windows.Forms.Label();
         this.buttonBackgroud = new System.Windows.Forms.Button();
         this.labelSDKVersion = new System.Windows.Forms.Label();
         this.checkBoxExposureTime = new System.Windows.Forms.CheckBox();
         this.labelExposureTime = new System.Windows.Forms.Label();
         this.buttonSaveBackGround = new System.Windows.Forms.Button();
         this.buttonLoadBackgroud = new System.Windows.Forms.Button();
         this.textBoxExposureTime = new System.Windows.Forms.TextBox();
         this.textBoxCanvasSize = new System.Windows.Forms.TextBox();
         this.labelCanvasSize = new System.Windows.Forms.Label();
         this.buttonClearBackGround = new System.Windows.Forms.Button();
         this.checkBoxCropImage = new System.Windows.Forms.CheckBox();
         this.checkBoxGrayScale = new System.Windows.Forms.CheckBox();
         ((System.ComponentModel.ISupportInitialize)(this.dataGridViewCameras)).BeginInit();
         ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).BeginInit();
         this.SuspendLayout();
         // 
         // buttonRunAll
         // 
         this.buttonRunAll.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonRunAll.Location = new System.Drawing.Point(109, 14);
         this.buttonRunAll.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonRunAll.Name = "buttonRunAll";
         this.buttonRunAll.Size = new System.Drawing.Size(91, 27);
         this.buttonRunAll.TabIndex = 1;
         this.buttonRunAll.Text = "Run All";
         this.buttonRunAll.UseVisualStyleBackColor = true;
         this.buttonRunAll.Click += new System.EventHandler(this.ButtonRun_Click);
         // 
         // buttonStopAll
         // 
         this.buttonStopAll.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonStopAll.Location = new System.Drawing.Point(205, 13);
         this.buttonStopAll.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonStopAll.Name = "buttonStopAll";
         this.buttonStopAll.Size = new System.Drawing.Size(96, 27);
         this.buttonStopAll.TabIndex = 1;
         this.buttonStopAll.Text = "Stop All";
         this.buttonStopAll.UseVisualStyleBackColor = true;
         this.buttonStopAll.Click += new System.EventHandler(this.ButtonStop_Click);
         // 
         // dataGridViewCameras
         // 
         this.dataGridViewCameras.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
         this.dataGridViewCameras.Location = new System.Drawing.Point(14, 177);
         this.dataGridViewCameras.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.dataGridViewCameras.Name = "dataGridViewCameras";
         this.dataGridViewCameras.RowHeadersWidthSizeMode = System.Windows.Forms.DataGridViewRowHeadersWidthSizeMode.AutoSizeToAllHeaders;
         this.dataGridViewCameras.Size = new System.Drawing.Size(529, 512);
         this.dataGridViewCameras.TabIndex = 3;
         this.dataGridViewCameras.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.DataGridViewCameras_CellContentClick);
         // 
         // buttonRun
         // 
         this.buttonRun.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonRun.Location = new System.Drawing.Point(14, 47);
         this.buttonRun.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonRun.Name = "buttonRun";
         this.buttonRun.Size = new System.Drawing.Size(88, 27);
         this.buttonRun.TabIndex = 1;
         this.buttonRun.Text = "Run ";
         this.buttonRun.UseVisualStyleBackColor = true;
         this.buttonRun.Click += new System.EventHandler(this.ButtonCamRun_Click);
         // 
         // buttonStop
         // 
         this.buttonStop.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonStop.Location = new System.Drawing.Point(109, 47);
         this.buttonStop.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonStop.Name = "buttonStop";
         this.buttonStop.Size = new System.Drawing.Size(91, 27);
         this.buttonStop.TabIndex = 1;
         this.buttonStop.Text = "Stop ";
         this.buttonStop.UseVisualStyleBackColor = true;
         this.buttonStop.Click += new System.EventHandler(this.ButtonCamStop_Click);
         // 
         // labelSelectedItem
         // 
         this.labelSelectedItem.AutoSize = true;
         this.labelSelectedItem.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.labelSelectedItem.Location = new System.Drawing.Point(543, 153);
         this.labelSelectedItem.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
         this.labelSelectedItem.Name = "labelSelectedItem";
         this.labelSelectedItem.Size = new System.Drawing.Size(63, 20);
         this.labelSelectedItem.TabIndex = 4;
         this.labelSelectedItem.Text = "Cam # :";
         // 
         // pictureBox
         // 
         this.pictureBox.Location = new System.Drawing.Point(545, 176);
         this.pictureBox.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.pictureBox.Name = "pictureBox";
         this.pictureBox.Size = new System.Drawing.Size(512, 512);
         this.pictureBox.TabIndex = 5;
         this.pictureBox.TabStop = false;
         // 
         // detectCamerasButton
         // 
         this.detectCamerasButton.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.detectCamerasButton.Location = new System.Drawing.Point(14, 14);
         this.detectCamerasButton.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.detectCamerasButton.Name = "detectCamerasButton";
         this.detectCamerasButton.Size = new System.Drawing.Size(88, 27);
         this.detectCamerasButton.TabIndex = 6;
         this.detectCamerasButton.Text = "Detect";
         this.detectCamerasButton.UseVisualStyleBackColor = true;
         this.detectCamerasButton.Click += new System.EventHandler(this.DectectCamerasButton_Click);
         // 
         // checkBoxAutoTracking
         // 
         this.checkBoxAutoTracking.AutoSize = true;
         this.checkBoxAutoTracking.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.checkBoxAutoTracking.Location = new System.Drawing.Point(547, 12);
         this.checkBoxAutoTracking.Name = "checkBoxAutoTracking";
         this.checkBoxAutoTracking.Size = new System.Drawing.Size(88, 44);
         this.checkBoxAutoTracking.TabIndex = 7;
         this.checkBoxAutoTracking.Text = "Auto \r\nTracking";
         this.checkBoxAutoTracking.UseVisualStyleBackColor = true;
         this.checkBoxAutoTracking.CheckedChanged += new System.EventHandler(this.CheckBoxAutoTracking_CheckedChanged);
         // 
         // labelTop
         // 
         this.labelTop.AutoSize = true;
         this.labelTop.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.labelTop.Location = new System.Drawing.Point(541, 98);
         this.labelTop.Name = "labelTop";
         this.labelTop.Size = new System.Drawing.Size(40, 20);
         this.labelTop.TabIndex = 8;
         this.labelTop.Text = "Top:";
         // 
         // checkBoxShowImage
         // 
         this.checkBoxShowImage.AutoSize = true;
         this.checkBoxShowImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.checkBoxShowImage.Location = new System.Drawing.Point(928, 12);
         this.checkBoxShowImage.Name = "checkBoxShowImage";
         this.checkBoxShowImage.Size = new System.Drawing.Size(73, 44);
         this.checkBoxShowImage.TabIndex = 7;
         this.checkBoxShowImage.Text = "Show\r\nImage";
         this.checkBoxShowImage.UseVisualStyleBackColor = true;
         this.checkBoxShowImage.CheckedChanged += new System.EventHandler(this.CheckBoxShowImage_CheckedChanged);
         // 
         // labelSize
         // 
         this.labelSize.AutoSize = true;
         this.labelSize.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.labelSize.Location = new System.Drawing.Point(541, 123);
         this.labelSize.Name = "labelSize";
         this.labelSize.Size = new System.Drawing.Size(61, 20);
         this.labelSize.TabIndex = 9;
         this.labelSize.Text = "Center:";
         // 
         // buttonBackgroud
         // 
         this.buttonBackgroud.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonBackgroud.Location = new System.Drawing.Point(15, 695);
         this.buttonBackgroud.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonBackgroud.Name = "buttonBackgroud";
         this.buttonBackgroud.Size = new System.Drawing.Size(96, 27);
         this.buttonBackgroud.TabIndex = 1;
         this.buttonBackgroud.Text = "BackGround";
         this.buttonBackgroud.UseVisualStyleBackColor = true;
         this.buttonBackgroud.Click += new System.EventHandler(this.ButtonBackground_Click);
         // 
         // labelSDKVersion
         // 
         this.labelSDKVersion.AutoSize = true;
         this.labelSDKVersion.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F);
         this.labelSDKVersion.Location = new System.Drawing.Point(12, 738);
         this.labelSDKVersion.Name = "labelSDKVersion";
         this.labelSDKVersion.Size = new System.Drawing.Size(105, 18);
         this.labelSDKVersion.TabIndex = 10;
         this.labelSDKVersion.Text = "SDK Version : ";
         // 
         // checkBoxExposureTime
         // 
         this.checkBoxExposureTime.AutoSize = true;
         this.checkBoxExposureTime.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.checkBoxExposureTime.Location = new System.Drawing.Point(664, 12);
         this.checkBoxExposureTime.Name = "checkBoxExposureTime";
         this.checkBoxExposureTime.Size = new System.Drawing.Size(133, 44);
         this.checkBoxExposureTime.TabIndex = 7;
         this.checkBoxExposureTime.Text = "Auto\r\nExposure Time";
         this.checkBoxExposureTime.UseVisualStyleBackColor = true;
         this.checkBoxExposureTime.CheckedChanged += new System.EventHandler(this.CheckBoxExposureTime_CheckedChanged);
         // 
         // labelExposureTime
         // 
         this.labelExposureTime.AutoSize = true;
         this.labelExposureTime.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.labelExposureTime.Location = new System.Drawing.Point(540, 74);
         this.labelExposureTime.Name = "labelExposureTime";
         this.labelExposureTime.Size = new System.Drawing.Size(118, 20);
         this.labelExposureTime.TabIndex = 8;
         this.labelExposureTime.Text = "Exposure Time:";
         // 
         // buttonSaveBackGround
         // 
         this.buttonSaveBackGround.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonSaveBackGround.Location = new System.Drawing.Point(122, 695);
         this.buttonSaveBackGround.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonSaveBackGround.Name = "buttonSaveBackGround";
         this.buttonSaveBackGround.Size = new System.Drawing.Size(133, 27);
         this.buttonSaveBackGround.TabIndex = 1;
         this.buttonSaveBackGround.Text = "Save BackGround";
         this.buttonSaveBackGround.UseVisualStyleBackColor = true;
         this.buttonSaveBackGround.Click += new System.EventHandler(this.ButtonSaveBackground_Click);
         // 
         // buttonLoadBackgroud
         // 
         this.buttonLoadBackgroud.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonLoadBackgroud.Location = new System.Drawing.Point(266, 695);
         this.buttonLoadBackgroud.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonLoadBackgroud.Name = "buttonLoadBackgroud";
         this.buttonLoadBackgroud.Size = new System.Drawing.Size(133, 27);
         this.buttonLoadBackgroud.TabIndex = 1;
         this.buttonLoadBackgroud.Text = "Load BackGround";
         this.buttonLoadBackgroud.UseVisualStyleBackColor = true;
         this.buttonLoadBackgroud.Click += new System.EventHandler(this.ButtonLoadBackground_Click);
         // 
         // textBoxExposureTime
         // 
         this.textBoxExposureTime.Location = new System.Drawing.Point(658, 74);
         this.textBoxExposureTime.Name = "textBoxExposureTime";
         this.textBoxExposureTime.Size = new System.Drawing.Size(66, 22);
         this.textBoxExposureTime.TabIndex = 11;
         this.textBoxExposureTime.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.TextBoxExposureTime_KeyPress);
         // 
         // textBoxCanvasSize
         // 
         this.textBoxCanvasSize.Location = new System.Drawing.Point(991, 153);
         this.textBoxCanvasSize.Name = "textBoxCanvasSize";
         this.textBoxCanvasSize.Size = new System.Drawing.Size(66, 22);
         this.textBoxCanvasSize.TabIndex = 11;
         this.textBoxCanvasSize.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.TextBoxCanvasSize_KeyPress);
         // 
         // labelCanvasSize
         // 
         this.labelCanvasSize.AutoSize = true;
         this.labelCanvasSize.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.labelCanvasSize.Location = new System.Drawing.Point(884, 153);
         this.labelCanvasSize.Name = "labelCanvasSize";
         this.labelCanvasSize.Size = new System.Drawing.Size(101, 20);
         this.labelCanvasSize.TabIndex = 8;
         this.labelCanvasSize.Text = "Canvas Size:";
         // 
         // buttonClearBackGround
         // 
         this.buttonClearBackGround.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.buttonClearBackGround.Location = new System.Drawing.Point(410, 695);
         this.buttonClearBackGround.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.buttonClearBackGround.Name = "buttonClearBackGround";
         this.buttonClearBackGround.Size = new System.Drawing.Size(133, 27);
         this.buttonClearBackGround.TabIndex = 1;
         this.buttonClearBackGround.Text = "Clear BackGround";
         this.buttonClearBackGround.UseVisualStyleBackColor = true;
         this.buttonClearBackGround.Click += new System.EventHandler(this.ButtonClearBackGround_Click);
         // 
         // checkBoxCropImage
         // 
         this.checkBoxCropImage.AutoSize = true;
         this.checkBoxCropImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.checkBoxCropImage.Location = new System.Drawing.Point(826, 12);
         this.checkBoxCropImage.Name = "checkBoxCropImage";
         this.checkBoxCropImage.Size = new System.Drawing.Size(73, 44);
         this.checkBoxCropImage.TabIndex = 7;
         this.checkBoxCropImage.Text = "Crop\r\nImage";
         this.checkBoxCropImage.UseVisualStyleBackColor = true;
         this.checkBoxCropImage.CheckedChanged += new System.EventHandler(this.CheckBoxCropImage_CheckedChanged);
         // 
         // checkBoxGrayScale
         // 
         this.checkBoxGrayScale.AutoSize = true;
         this.checkBoxGrayScale.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.checkBoxGrayScale.Location = new System.Drawing.Point(752, 74);
         this.checkBoxGrayScale.Name = "checkBoxGrayScale";
         this.checkBoxGrayScale.Size = new System.Drawing.Size(102, 24);
         this.checkBoxGrayScale.TabIndex = 7;
         this.checkBoxGrayScale.Text = "GrayScale";
         this.checkBoxGrayScale.UseVisualStyleBackColor = true;
         this.checkBoxGrayScale.CheckedChanged += new System.EventHandler(this.checkBoxGrayScale_CheckedChanged);
         // 
         // MainForm
         // 
         this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
         this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
         this.ClientSize = new System.Drawing.Size(1070, 770);
         this.Controls.Add(this.textBoxCanvasSize);
         this.Controls.Add(this.textBoxExposureTime);
         this.Controls.Add(this.labelSDKVersion);
         this.Controls.Add(this.labelSize);
         this.Controls.Add(this.labelCanvasSize);
         this.Controls.Add(this.labelExposureTime);
         this.Controls.Add(this.labelTop);
         this.Controls.Add(this.checkBoxExposureTime);
         this.Controls.Add(this.checkBoxCropImage);
         this.Controls.Add(this.checkBoxGrayScale);
         this.Controls.Add(this.checkBoxShowImage);
         this.Controls.Add(this.checkBoxAutoTracking);
         this.Controls.Add(this.detectCamerasButton);
         this.Controls.Add(this.pictureBox);
         this.Controls.Add(this.labelSelectedItem);
         this.Controls.Add(this.dataGridViewCameras);
         this.Controls.Add(this.buttonClearBackGround);
         this.Controls.Add(this.buttonLoadBackgroud);
         this.Controls.Add(this.buttonSaveBackGround);
         this.Controls.Add(this.buttonBackgroud);
         this.Controls.Add(this.buttonStop);
         this.Controls.Add(this.buttonStopAll);
         this.Controls.Add(this.buttonRun);
         this.Controls.Add(this.buttonRunAll);
         this.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
         this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
         this.Name = "MainForm";
         this.Text = "Beamage SDK Example V1.02.02";
         this.Load += new System.EventHandler(this.MainForm_Load);
         ((System.ComponentModel.ISupportInitialize)(this.dataGridViewCameras)).EndInit();
         ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).EndInit();
         this.ResumeLayout(false);
         this.PerformLayout();

      }

      #endregion
      private System.Windows.Forms.Button buttonRunAll;
      private System.Windows.Forms.Button buttonStopAll;
      private System.Windows.Forms.DataGridView dataGridViewCameras;
      private System.Windows.Forms.Button buttonRun;
      private System.Windows.Forms.Button buttonStop;
      private System.Windows.Forms.Label labelSelectedItem;
      private System.Windows.Forms.PictureBox pictureBox;
        private System.Windows.Forms.Button detectCamerasButton;
        private System.Windows.Forms.CheckBox checkBoxAutoTracking;
        private System.Windows.Forms.Label labelTop;
        private System.Windows.Forms.CheckBox checkBoxShowImage;
        private System.Windows.Forms.Label labelSize;
        private System.Windows.Forms.Button buttonBackgroud;
        private System.Windows.Forms.Label labelSDKVersion;
        private System.Windows.Forms.CheckBox checkBoxExposureTime;
        private System.Windows.Forms.Label labelExposureTime;
        private System.Windows.Forms.Button buttonSaveBackGround;
        private System.Windows.Forms.Button buttonLoadBackgroud;
        private System.Windows.Forms.TextBox textBoxExposureTime;
        private System.Windows.Forms.TextBox textBoxCanvasSize;
        private System.Windows.Forms.Label labelCanvasSize;
        private System.Windows.Forms.Button buttonClearBackGround;
        private System.Windows.Forms.CheckBox checkBoxCropImage;
		private System.Windows.Forms.CheckBox checkBoxGrayScale;
	}
}

