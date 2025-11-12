
// NamedPipeClientDlg.h : header file
//

#pragma once


// CNamedPipeClientDlg dialog
class CNamedPipeClientDlg : public CDialogEx
{
// Construction
public:
	CNamedPipeClientDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_NAMEDPIPECLIENT_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support

	CFile		m_File;
	int		m_bOpenPipe;
	CString  m_strFocalLength;
	CStatic	m_BmpViewer;
	CButton	m_checkBmp;
	CButton	m_checkJpg;
	CEdit		m_editFocalLength;


// TIMER
#define CAPTURING					(1)
#define GET_AXIS					(2)

// TIMER TIMING
#define TIMER_CAPTURE			(50)
#define TIMER_AXIS				(300)

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();

	DECLARE_MESSAGE_MAP()

public:

	void GetSigmaXAxis();
	void GetSigmaYAxis();
	void GetCentroidXAxis();
	void GetCentroidYAxis();
	void GetPeakSaturationLevel();
	void Get2DImage(CString command, int count, int control);

	afx_msg void OnBnClickedButtonRun();
	afx_msg void OnBnClickedButtonOpenPipe();
	afx_msg void OnBnClickedButtonSerialNumber();
	afx_msg void OnBnClickedButtonClose();
	afx_msg void OnBnClickedButtonCentroidX();
	afx_msg void OnBnClickedButtonCentroidY();
	afx_msg void OnBnClickedButtonPeakSaturation();
	afx_msg void OnBnClickedButtonSigmaXAxis();
	afx_msg void OnBnClickedButtonSigmaYAxis();
	

	afx_msg void OnBnClickedButton4Sigma();
	afx_msg void OnBnClickedButtonFWHM();
	afx_msg void OnBnClickedButtonGetImage();


	afx_msg void OnBnClickedButtonStartCaptureImage();
	afx_msg void OnBnClickedButtonStopCaptureImage();
	afx_msg void OnBnClickedButtonAbout();

	afx_msg void OnTimer(UINT_PTR nIDEvent);

	afx_msg void OnBnClickedButtonTrigger();
	afx_msg void OnBnClickedButtonSaveCurrentImage();
	afx_msg void OnBnClickedCheckBmp();
	afx_msg void OnBnClickedCheckJpg();
	afx_msg void OnBnClickedButtonDivergence();
	afx_msg void OnBnClickedButtonDivergenceX();
	afx_msg void OnBnClickedButtonDivergenceY();
	afx_msg void OnBnClickedButtonSendFocalLength();
	afx_msg void OnBnClickedButtonActGrayScale();
	afx_msg void OnBnClickedButtonIrFilter();
	afx_msg void OnBnClickedButtonDespeckleFilter();
	afx_msg void OnBnClickedButtonSmoothingFilter();
	afx_msg void OnBnClickedButtonNormalize();
};
