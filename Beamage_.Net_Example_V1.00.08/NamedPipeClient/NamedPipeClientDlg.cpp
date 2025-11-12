
// NamedPipeClientDlg.cpp : implementation file
//

#include "stdafx.h"
#include "NamedPipeClient.h"
#include "NamedPipeClientDlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CAboutDlg dialog used for App About

//////////////////////////////////////////////////////////////////////////
class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

//////////////////////////////////////////////////////////////////////////
CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD) {

}

//////////////////////////////////////////////////////////////////////////
void CAboutDlg::DoDataExchange(CDataExchange* pDX) {

	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


//////////////////////////////////////////////////////////////////////////
CNamedPipeClientDlg::CNamedPipeClientDlg(CWnd* pParent /*=NULL*/) : CDialogEx(CNamedPipeClientDlg::IDD, pParent) {

	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
	m_bOpenPipe = 0;
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_STATIC_BMP,					m_BmpViewer);
	DDX_Control(pDX, IDC_CHECK_BMP,					m_checkBmp);
	DDX_Control(pDX, IDC_CHECK_JPG,					m_checkJpg);
	DDX_Control(pDX, IDC_EDIT_FOCAL_LENGTH,		m_editFocalLength);
}

BEGIN_MESSAGE_MAP(CNamedPipeClientDlg, CDialogEx)

	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_TIMER()

	ON_BN_CLICKED(IDC_BUTTON_RUN,					&CNamedPipeClientDlg::OnBnClickedButtonRun)
	ON_BN_CLICKED(IDC_BUTTON_OPEN_PIPE,			&CNamedPipeClientDlg::OnBnClickedButtonOpenPipe)
	ON_BN_CLICKED(IDC_BUTTON_SERIAL_NUMBER,	&CNamedPipeClientDlg::OnBnClickedButtonSerialNumber)
	ON_BN_CLICKED(IDC_BUTTON_CLOSE,				&CNamedPipeClientDlg::OnBnClickedButtonClose)
	ON_BN_CLICKED(IDC_BUTTON_CENTROID_X,		&CNamedPipeClientDlg::OnBnClickedButtonCentroidX)
	ON_BN_CLICKED(IDC_BUTTON_CENTROID_Y,		&CNamedPipeClientDlg::OnBnClickedButtonCentroidY)
	ON_BN_CLICKED(IDC_BUTTON_PEAK_SATURATION,	&CNamedPipeClientDlg::OnBnClickedButtonPeakSaturation)
	ON_BN_CLICKED(IDC_BUTTON_SIGMA_X_AXIS,		&CNamedPipeClientDlg::OnBnClickedButtonSigmaXAxis)
	ON_BN_CLICKED(IDC_BUTTON_SIGMA_Y_AXIS,		&CNamedPipeClientDlg::OnBnClickedButtonSigmaYAxis)
	ON_BN_CLICKED(IDC_BUTTON_1E2,					&CNamedPipeClientDlg::OnBnClickedButton4Sigma)
	ON_BN_CLICKED(IDC_BUTTON_FWHM,				&CNamedPipeClientDlg::OnBnClickedButtonFWHM)

	ON_BN_CLICKED(IDC_BUTTON_GET_IMAGE,			&CNamedPipeClientDlg::OnBnClickedButtonGetImage)
	ON_BN_CLICKED(IDC_BUTTON_START_CAPTURE,	&CNamedPipeClientDlg::OnBnClickedButtonStartCaptureImage)
	ON_BN_CLICKED(IDC_BUTTON_STOP_CAPTURE,		&CNamedPipeClientDlg::OnBnClickedButtonStopCaptureImage)

	ON_BN_CLICKED(IDC_BUTTON_ABOUT,					&CNamedPipeClientDlg::OnBnClickedButtonAbout)
	ON_BN_CLICKED(IDC_BUTTON_TRIGGER,				&CNamedPipeClientDlg::OnBnClickedButtonTrigger)
	ON_BN_CLICKED(IDC_BUTTON_SAVE_CURRENT_IMAGE, &CNamedPipeClientDlg::OnBnClickedButtonSaveCurrentImage)
	ON_BN_CLICKED(IDC_CHECK_BMP,						&CNamedPipeClientDlg::OnBnClickedCheckBmp)
	ON_BN_CLICKED(IDC_CHECK_JPG,						&CNamedPipeClientDlg::OnBnClickedCheckJpg)
	ON_BN_CLICKED(IDC_BUTTON_DIVERGENCE,			&CNamedPipeClientDlg::OnBnClickedButtonDivergence)
	ON_BN_CLICKED(IDC_BUTTON_DIVERGENCE_X,			&CNamedPipeClientDlg::OnBnClickedButtonDivergenceX)
	ON_BN_CLICKED(IDC_BUTTON_DIVERGENCE_Y,			&CNamedPipeClientDlg::OnBnClickedButtonDivergenceY)
	ON_BN_CLICKED(IDC_BUTTON_SEND_FOCAL_LENGTH,	&CNamedPipeClientDlg::OnBnClickedButtonSendFocalLength)
	ON_BN_CLICKED(IDC_BUTTON_ACT_GS,					&CNamedPipeClientDlg::OnBnClickedButtonActGrayScale)
	ON_BN_CLICKED(IDC_BUTTON_IR_FILTER, &CNamedPipeClientDlg::OnBnClickedButtonIrFilter)
	ON_BN_CLICKED(IDC_BUTTON_DESPECKLE_FILTER, &CNamedPipeClientDlg::OnBnClickedButtonDespeckleFilter)
	ON_BN_CLICKED(IDC_BUTTON_SMOOTHING_FILTER, &CNamedPipeClientDlg::OnBnClickedButtonSmoothingFilter)
	ON_BN_CLICKED(IDC_BUTTON_NORMALIZE, &CNamedPipeClientDlg::OnBnClickedButtonNormalize)
END_MESSAGE_MAP()


////////////////////////////////////////////////////////////////////////////////
BOOL CNamedPipeClientDlg::OnInitDialog() {

	CDialogEx::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here

	m_checkBmp.SetCheck(true);
	m_checkJpg.SetCheck(false);
	m_strFocalLength = _T("");

	return TRUE;  // return TRUE  unless you set the focus to a control
}

////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX) {

		CAboutDlg dlgAbout;
		dlgAbout.DoModal();

	} else {

		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnPaint()
{
	if (IsIconic())	{

		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);

	} else {

		CDialogEx::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CNamedPipeClientDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}

////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonClose() {

	if (m_bOpenPipe) {

		m_bOpenPipe = 0;

		m_File.Close();
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonAbout()
{
	AfxMessageBox(_T("Named Pipe Client V1.00.06"),MB_ICONINFORMATION);
}

////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonCentroidX()
{
	GetCentroidXAxis();
}

////////////////////////////////////////////////////////////////////////////////

void CNamedPipeClientDlg::OnBnClickedButtonCentroidY()
{
	GetCentroidYAxis();
}


////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonPeakSaturation()
{
	GetPeakSaturationLevel();
}


////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSigmaXAxis()
{
	GetSigmaXAxis();
}


//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSigmaYAxis()
{
	GetSigmaYAxis();
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedCheckBmp()
{
	m_checkJpg.SetCheck(false);
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedCheckJpg()
{
	m_checkBmp.SetCheck(false);
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::Get2DImage(CString command, int count, int control)
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(command, count * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(control, CString(lpszBuffer));

		// get the my document path
		TCHAR pf[MAX_PATH];
		SHGetSpecialFolderPath(0, pf, CSIDL_MYDOCUMENTS, FALSE);

		CString folderPath = pf;
		folderPath = folderPath + _T("\\Gentec-EO");

		// complete the folder path
		folderPath = folderPath + _T("\\beamage.bmp");

		// load image to the application
		CImage image;
		image.Load(folderPath);
		CBitmap bitmap;
		bitmap.Attach(image.Detach());

		m_BmpViewer.SetBitmap(HBITMAP(bitmap));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonRun() {

	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];
	
		m_File.Write(_T("*CTLSTART"), 9*sizeof(TCHAR));
	
		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_RUN, CString(lpszBuffer));
	}
}

////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonOpenPipe() {

	if (m_bOpenPipe == 0) {

		int bResult = m_File.Open(_T("\\\\.\\pipe\\pipe_beamage"), CFile::modeReadWrite);

		if (bResult) AfxMessageBox(_T("File opened"));
		else		 AfxMessageBox(_T("File NOT opened"));

		m_bOpenPipe = 1;
	} 
}

////////////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSerialNumber() {

	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEASNM"), 8 * sizeof(TCHAR));
	
		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_SERIAL_NUMBER, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButton4Sigma() {

	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*CTL4SIG"), 9*sizeof(TCHAR));
	
		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_MAIN_CONTROL, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonFWHM() {

	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*CTLFWHM"), 9 * sizeof(TCHAR));
	
		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_MAIN_CONTROL, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonGetImage()
{
	Get2DImage(_T("*CTLBMPSAVE"),12, IDC_EDIT_GET_IMAGE);
}


//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonStartCaptureImage()
{

	SetTimer(CAPTURING, TIMER_CAPTURE, NULL);
	SetTimer(GET_AXIS, TIMER_AXIS, NULL);
	
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonStopCaptureImage()
{
	KillTimer(CAPTURING);
	KillTimer(GET_AXIS);

}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnTimer(UINT_PTR nIDEvent)
{
	switch (nIDEvent) {

	case CAPTURING:

		Get2DImage(_T("*CTLBMPSAVE"), 12, IDC_EDIT_START_CAPTURE);

		break;

	case GET_AXIS : 

		GetSigmaXAxis();
		GetSigmaYAxis();
		GetCentroidXAxis();
		GetCentroidYAxis();
		GetPeakSaturationLevel();

		break;

	default:
		break;
	}

	CDialogEx::OnTimer(nIDEvent);
}



//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::GetSigmaXAxis()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEASIXAX"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_SIGMA_X, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::GetSigmaYAxis()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEASIYAX"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_SIGMA_Y, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::GetCentroidXAxis()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEACENTX"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_CENTROID_X, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::GetCentroidYAxis()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEACENTY"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_CENTROID_Y, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::GetPeakSaturationLevel()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEAPKSAT"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_PEAK_SATURATION_LEVEL, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonTrigger()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTTRIG"), 9 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_TRIGGER, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSaveCurrentImage()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];
		CString command = _T("");

		if (m_checkBmp.GetCheck())
			command = _T("*CTLBMPSAVE");
		else 
			command = _T("*CTLJPGSAVE");

		m_File.Write(command, 12 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_SAVE_CURRENT_IMAGE, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonDivergence()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTDIVER"), 10 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_DIVERGENCE, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonDivergenceX()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEAXDIVER"), 11 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_DIVERGENCE_X, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonDivergenceY()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*MEAYDIVER"), 11 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_DIVERGENCE_Y, CString(lpszBuffer));
	}

	
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSendFocalLength()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_editFocalLength.GetWindowTextW(m_strFocalLength);

		m_File.Write(_T("*SNDFLDIVER" + m_strFocalLength), 24 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonActGrayScale()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTGSCALE"), 11 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_GRAY_SCALE, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonIrFilter()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTIRF"), 8 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_IR_FILTER, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonDespeckleFilter()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTDESPECF"), 12 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_DESPECKLE_FILTER, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonSmoothingFilter()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTSMOOTF"), 11 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_SMOOTHING_FILTER, CString(lpszBuffer));
	}
}

//////////////////////////////////////////////////////////////////////////
void CNamedPipeClientDlg::OnBnClickedButtonNormalize()
{
	if (m_bOpenPipe) {

		TCHAR lpszBuffer[4096];

		m_File.Write(_T("*ACTNORMALI"), 12 * sizeof(TCHAR));

		m_File.Read(lpszBuffer, 4096);

		SetDlgItemText(IDC_EDIT_NORMALIZE, CString(lpszBuffer));
	}
}
