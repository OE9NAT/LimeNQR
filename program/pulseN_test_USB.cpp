/**
  @file   N pulses
  @author Andrin Doll
  @brief  N pulses on TX and collection on RX


requirements:
LimeSuite
HDF5 library

compilation:
g++ pulseN_test_USB.cpp -std=c++11 -lLimeSuite -o pulseN_test_USB -I/usr/include/hdf5/serial -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -fstack-protector-strong -Wformat -Werror=format-security -L/usr/lib/x86_64-linux-gnu/hdf5/serial /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5_hl_cpp.a /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5_cpp.a /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5_hl.a /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5.a -Wl,-Bsymbolic-functions -Wl,-z,relro -lpthread -lsz -lz -ldl -lm -Wl,-rpath -Wl,/usr/lib/x86_64-linux-gnu/hdf5/serial


Installation note: this compilation line looks terrifyingly long.. The reason is the inclusion of the HDF5 library, which is responsible for all the arguments after the -o specification. All this arguments can actually be retrieved from the command:
h5c++ -show

 */
#include "lime/LimeSuite.h"
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <chrono>
#include <list>
#include <iomanip> 
#include <sstream> 
#include "H5Cpp.h"

#include <sys/stat.h> // stat
#include <sys/types.h> 
#include <errno.h>    // errno, ENOENT, EEXIST
#if defined(_WIN32)
#include <direct.h>   // _mkdir
#endif

using namespace std;

// structure that holds all the relevant parameters for a N-pulse experiment. See initialization below for description
const int maxNpulse = 50;
struct LimeConfig_t {

	float 	srate;
	float 	frq;
	float 	frq_set;
	float	RX_LPF;
	float	TX_LPF;
	int	RX_gain;
	int	TX_gain;
	int	TX_IcorrDC;
	int	TX_QcorrDC;
	int	TX_IcorrGain;
	int	TX_QcorrGain;
	int	TX_IQcorrPhase;
	int	RX_IcorrGain;
	int	RX_QcorrGain;
	int	RX_IQcorrPhase;
	int	RX_gain_rback[4];
	int	TX_gain_rback[3];

	int	Npulses;
	double	*p_dur;
	int	*p_dur_smp;
	int	*p_offs;
	double 	*p_amp;
	double 	*p_frq;
	double 	*p_frq_smp;
	double 	*p_pha;
	int 	*p_phacyc_N;
	int 	*p_phacyc_lev;
	double 	*am_frq;
	double 	*am_pha;
	double 	*am_depth;
	int 	*am_mode;
	double 	*am_frq_smp;
	double 	*fm_frq;
	double 	*fm_pha;
	double 	*fm_width;
	int 	*fm_mode;
	double 	*fm_frq_smp;

	int	*p_c0_en;
	int	*p_c1_en;
	int	*p_c2_en;
	int	*p_c3_en;

	int 	c0_tim[4];
	int 	c1_tim[4];
	int 	c2_tim[4];
	int 	c3_tim[4];

	int 	c0_synth[5];
	int 	c1_synth[5];
	int 	c2_synth[5];
	int 	c3_synth[5];

	int 	averages;
	int 	repetitions;
	int 	pcyc_bef_avg;
	double	reptime_secs;
	double	rectime_secs;
	int	reptime_smps;
	int	rectime_smps;
	int	buffersize;
	
	string 	file_pattern;
	string 	file_stamp;
	string 	save_path;
	int	override_save;
	int	override_init;

	string 	stamp_start;
	string 	stamp_end;
};

// structure that will be used to map LimeConfig to HDF attribute
struct Config2HDFattr_t {
	string		arg;
	H5std_string 	Name;
	H5::DataType	dType;
	void *		Value;
	hsize_t 	dim;
};

//Device structure, should be initialize to NULL
static lms_device_t* device = NULL;

// LMS error function
int error()
{
	if (device != NULL)
		LMS_Close(device);
	exit(-1);
}

// portable way to check and create directory (from stackexchange)
// https://stackoverflow.com/questions/675039/how-can-i-create-directory-tree-in-c-linux
bool isDirExist(const std::string& path)
{
#if defined(_WIN32)
	struct _stat info;
	if (_stat(path.c_str(), &info) != 0) { return false; }
	return (info.st_mode & _S_IFDIR) != 0;
#else 
	struct stat info;
	if (stat(path.c_str(), &info) != 0) { return false; }
	return (info.st_mode & S_IFDIR) != 0;
#endif
}

bool makePath(const std::string& path)
{
#if defined(_WIN32)
	int ret = _mkdir(path.c_str());
#else
	mode_t mode = 0755;
	int ret = mkdir(path.c_str(), mode);
#endif
	if (ret == 0) return true;

	switch (errno)
	{
		case ENOENT:
			// parent didn't exist, try to create it
			{
				int pos = path.find_last_of('/');
				if (pos == std::string::npos)
#if defined(_WIN32)
					pos = path.find_last_of('\\');
				if (pos == std::string::npos)
#endif
					return false;
				if (!makePath( path.substr(0, pos) ))
					return false;
			}
			// now, try to create again
#if defined(_WIN32)
			return 0 == _mkdir(path.c_str());
#else 
			return 0 == mkdir(path.c_str(), mode);
#endif

		case EEXIST:
			// done!
			return isDirExist(path);

		default:
			return false;
	}
}

inline bool file_exists (const std::string& name) {
  struct stat buffer;   
  return (stat (name.c_str(), &buffer) == 0); 
}

// Custom function to read back the gain of the RX/TX channels. The API function GetGaindB has to be avoided, 
// as it also modifies the gain, which is useless and dangerous..
//int GetGainRXTX(array< int, 4>* RXgain, array<int,3>* TXgain) {
int GetGainRXTX(int* RXgain, int* TXgain) {
	// RX gain: LNA, TIA and PGA
	uint16_t gain_lna, gain_tia, gain_pga;
	if (LMS_ReadParam(device, LMS7_G_LNA_RFE, &gain_lna) != 0) error();
	if (LMS_ReadParam(device, LMS7_G_TIA_RFE, &gain_tia) != 0) error();
	if (LMS_ReadParam(device, LMS7_G_PGA_RBB, &gain_pga) != 0) error();
	// convert to actual gain

	// TX gain: PAD and TBB
	uint16_t gain_pad, gain_tbb;
	if (LMS_ReadParam(device, LMS7_LOSS_LIN_TXPAD_TRF, &gain_pad) != 0) error();
	if (LMS_ReadParam(device, LMS7_CG_IAMP_TBB, &gain_tbb) != 0) error();

	// convert to actual gain
	// TXpad
	const int pmax = 52;
	if (gain_pad > 10) TXgain[1] = pmax-10-2*(gain_pad-10);
	else TXgain[1] = pmax-gain_pad;

	// TBB gain: linear to dB. Impossible to obtain like this. It is calibrated to an optimum value, called opt_gain_tbb. This is only available if a calibration is done. However, as long as the TXgain is below 43+12 = 55 dB, gain is fully determined by TX PAD
	TXgain[2] = gain_tbb;
	// TXgain[2] = 20.0*log10((float_type)gain_tbb / (float_type) opt_gain_tbb); from LMS7002.cpp

	// RFE LNA
	int gmax = 30;
	if (gain_lna >= 9) 
		RXgain[1] = gmax + (gain_lna-15);
	 else
		RXgain[1] = gmax + 3*( gain_lna - 11);

	// RFE TIA
	gmax = 12;
	switch (gain_tia)
	{
		case 3: RXgain[2] = gmax-0; break;
		case 2: RXgain[2] = gmax-3; break;
		case 1: RXgain[2] = gmax-12; break;
	}

	// RBB PGA
	RXgain[3] = gain_pga - 12;

	// Sum to first element, adding that mysterious +12+0.5 as it is done in the API
	RXgain[0] = RXgain[1] + RXgain[2] + RXgain[3] + 12 + 0.5;
	TXgain[0] = TXgain[1] + 0*TXgain[2] + 12 + 0.5; 

	// Print in function to ease debugging
	cout << "TX: " << TXgain[0] << " dB : " << TXgain[1] << " dB PAD, " << TXgain[2] << " setting of BB + 12 dB" << endl;
	cout << "RX: " << RXgain[0] << " dB : " << RXgain[1] << " dB LNA, " << RXgain[2] << " dB TIA, " << RXgain[3] << " dB PGA + 12 dB" << endl;

	return 0;
}

// Modulation function for AM/FM using different modes, i.e. sinusoidal (mode = 0), triangular (mode = 1), square (mode = 2)
double Modfunction(double argument, int mode) {

	const double pi = acos(-1);
	double P;

	double retval;
	switch (mode) {
		case 0: 
		{ // sinusoidal
			retval = cos(argument);
			break;
		}
		case 1: 
		{ // triangular

			// A = 2.0; P = np.pi
			// y = (A/P) * (P - abs(np.mod(x+np.pi/2,2*P)-P)) - A/2
			P = pi/2;
			retval = (2.0 / P) * (P - fabs(fmod(argument+pi/2,2*P)-P)) - 1.0;
			break;
		}
		case 2: 
		{ // square
			retval = (fmod(argument,2*pi) < pi) ? 1.0 : -1.0;
			break;
		}
		default: 
		{
			retval = 1.0;
			break;
		}
	}

	return retval;

}


int main(int argc, char** argv)
{
	const double pi = acos(-1);



	LimeConfig_t LimeCfg;

	LimeCfg.Npulses		= 2;		// Number of pulses, default value

	// check if nPulses has been given as argument, so that all the arrays are initialized with proper size
	for (int ii_arg = 1; ii_arg < argc; ii_arg++) {
		if (strcmp(argv[ii_arg], "-npu") == 0 && ii_arg + 1 < argc) {
			LimeCfg.Npulses = atoi(argv[ii_arg+1]);
			break;
		}
	}

	// ----------------------------------------------------------------------------------
	// set all the DEFAULT parameters. Command line arguments allow for modification!
	LimeCfg.srate 		= 30.72e6;	// sample rate of the IF DAC/ADC
	LimeCfg.frq 		= 50e6;		// LO carrier frequency
	LimeCfg.RX_gain		= 20;		// total gain of the receiver
	LimeCfg.TX_gain		= 30;		// total gain of the transmitter
	LimeCfg.RX_LPF		= 5e6;		// IF lowpass of the receiver
	LimeCfg.TX_LPF		= 130e6;	// IF lowpass of the transmitter

	LimeCfg.TX_IcorrDC	= -32;		// DC corr to TX mixer at IF (evaluate with LimeSuiteGUI)
	LimeCfg.TX_QcorrDC	=  50;		// DC corr to TX mixer at IF
	LimeCfg.TX_IcorrGain	= 2047;		// I Gain corr of TX mixer
	LimeCfg.TX_QcorrGain	= 2039;		// Q Gain corr of TX mixer
	LimeCfg.TX_IQcorrPhase	= 10;		// Phase corr of TX mixer
	LimeCfg.RX_IcorrGain	= 2047;		// I Gain corr of RX mixer
	LimeCfg.RX_QcorrGain	= 2047;		// Q Gain corr of RX mixer
	LimeCfg.RX_IQcorrPhase	= 0;		// Phase corr of RX mixer

	// Allocate the arrays with pulse parametes
	LimeCfg.p_dur		= new double[LimeCfg.Npulses];	// pulse duration (secs) 
	LimeCfg.p_offs		= new int[LimeCfg.Npulses];	// pulse time offset
	LimeCfg.p_amp		= new double[LimeCfg.Npulses];	// pulse digital IF amplitude
	LimeCfg.p_frq		= new double[LimeCfg.Npulses];	// pulse digital IF frequency (unit: Hz)
	LimeCfg.p_pha		= new double[LimeCfg.Npulses];	// pulse digital IF phase
	LimeCfg.p_phacyc_N	= new int[LimeCfg.Npulses];	// number of pulse phases (cycled within 2*pi, must be at least 1)
	LimeCfg.p_phacyc_lev	= new int[LimeCfg.Npulses];	// stacking level of phase cycle (for eventual coupling)
	LimeCfg.p_c0_en		= new int[LimeCfg.Npulses];	// pulse-wise enable of marker c0
	LimeCfg.p_c1_en		= new int[LimeCfg.Npulses];	// pulse-wise enable of marker c1
	LimeCfg.p_c2_en		= new int[LimeCfg.Npulses];	// pulse-wise enable of marker c2
	LimeCfg.p_c3_en		= new int[LimeCfg.Npulses];	// pulse-wise enable of marker c3
	LimeCfg.am_frq 		= new double[LimeCfg.Npulses];	// pulse AM frequency
	LimeCfg.am_pha 		= new double[LimeCfg.Npulses];	// pulse AM phase
	LimeCfg.am_depth	= new double[LimeCfg.Npulses];	// pulse AM depth
	LimeCfg.am_mode		= new int[LimeCfg.Npulses];	// pulse AM mode (0: sinus, 1: triangle, 2: square)
	LimeCfg.fm_frq 		= new double[LimeCfg.Npulses];	// pulse FM frequency
	LimeCfg.fm_pha 		= new double[LimeCfg.Npulses];	// pulse FM phase
	LimeCfg.fm_width	= new double[LimeCfg.Npulses];	// pulse FM width
	LimeCfg.fm_mode		= new int[LimeCfg.Npulses];	// pulse FM mode (0: sinus, 1: triangle, 2: square)

	// and set standard values
	for (int ii = 0; ii < LimeCfg.Npulses; ii++) {

		LimeCfg.p_dur[ii] 	= 2e-6;
		LimeCfg.p_offs[ii] 	= (4080*3)/(LimeCfg.Npulses+1);  // distribute them evenly within the buffer...
		LimeCfg.p_amp[ii]	= 1.0;
		LimeCfg.p_frq[ii] 	= 4.0/LimeCfg.p_dur[0];
		LimeCfg.p_pha[ii]	= 0.0;
		LimeCfg.p_phacyc_N[ii]	= 1;
		LimeCfg.p_phacyc_lev[ii]= 0;
		LimeCfg.p_c0_en[ii]	= 1;
		LimeCfg.p_c1_en[ii]	= 1;
		LimeCfg.p_c2_en[ii]	= 1;
		LimeCfg.p_c3_en[ii]	= 1;
		LimeCfg.am_frq[ii]	= 0;
		LimeCfg.am_pha[ii]	= 0;
		LimeCfg.am_depth[ii]	= 0;
		LimeCfg.am_mode[ii]	= 0;
		LimeCfg.fm_frq[ii]	= 0;
		LimeCfg.fm_pha[ii]	= 0;
		LimeCfg.fm_width[ii]	= 0;
		LimeCfg.fm_mode[ii]	= 0;
	}

	// Timing of TTL controls: [enabled? , pre, offs, post]
	int c0_tim[4]    	= {0,	70,	56,	-5};
	int c1_tim[4]    	= {0,	70,	56,	-5};
	int c2_tim[4]    	= {0,	70,	56,	-5};
	int c3_tim[4]    	= {0,	70,	56,	-5};

	// Use TTL channel as synth: [enabled? , half-period, strt, PSK shift, PSK adv]
	int c0_synth[5]    	= {0,	500,	0,	0,	0};
	int c1_synth[5]    	= {0,	500,	0,	0,	0};
	int c2_synth[5]    	= {0,	500,	0,	0,	0};
	int c3_synth[5]    	= {0,	500,	0,	0,	0};

	LimeCfg.averages	= 6;		// number of averages
	LimeCfg.repetitions	= 4;		// number of repetions
	LimeCfg.reptime_secs	= 4e-3;		// repetition time
	LimeCfg.rectime_secs	= 0.2e-3;	// duration of acquisition window
	LimeCfg.buffersize	= 4080 * 3;	// number of samples in buffer
	LimeCfg.pcyc_bef_avg 	= 0;		// phase cycle before average

	LimeCfg.file_pattern	= "test";	// identifier when saving the file
	LimeCfg.save_path	= "./asdf/";	// path to save the file to
	LimeCfg.override_save	= 0;		// default: save data
	LimeCfg.override_init	= 0;		// default: init LimeSDR


	// that's it for the parameters
	// ----------------------------------------------------------------------------------

	// .. copy here those arrays ...
	memcpy(LimeCfg.c0_tim, c0_tim, 4* sizeof *LimeCfg.c0_tim);
	memcpy(LimeCfg.c1_tim, c1_tim, 4* sizeof *LimeCfg.c1_tim);
	memcpy(LimeCfg.c2_tim, c2_tim, 4* sizeof *LimeCfg.c2_tim);
	memcpy(LimeCfg.c3_tim, c3_tim, 4* sizeof *LimeCfg.c3_tim);
	memcpy(LimeCfg.c0_synth, c0_synth, 5* sizeof *LimeCfg.c0_synth);
	memcpy(LimeCfg.c1_synth, c1_synth, 5* sizeof *LimeCfg.c1_synth);
	memcpy(LimeCfg.c2_synth, c2_synth, 5* sizeof *LimeCfg.c2_synth);
	memcpy(LimeCfg.c3_synth, c3_synth, 5* sizeof *LimeCfg.c3_synth);

	// and add the timestamp for the file 
	auto now = std::chrono::system_clock::now(); 
	auto itt = std::chrono::system_clock::to_time_t(now); 
	std::ostringstream stringstream;
	stringstream << std::put_time(localtime(&itt), "%G%m%d_%H%M%S");
	LimeCfg.file_stamp	= stringstream.str();
	LimeCfg.stamp_start	= stringstream.str();
	LimeCfg.stamp_end	= stringstream.str(); // will be overwritten just before data is written

	// allocate other variables that depend on Npulses
	LimeCfg.p_dur_smp = 	new int[LimeCfg.Npulses];
	LimeCfg.p_frq_smp = 	new double[LimeCfg.Npulses];
	LimeCfg.am_frq_smp = 	new double[LimeCfg.Npulses];
	LimeCfg.fm_frq_smp = 	new double[LimeCfg.Npulses];

	// LimeCfg as attributes for writing to HDF and for parsing command line input
	// This is all done 'manually', since there is no reflection in cpp.. at least not by default
	struct Config2HDFattr_t HDFattr[] = {
		{"sra",	"SampleRate [Hz]",	H5::PredType::IEEE_F32LE,	&LimeCfg.srate,		1},
		{"lof",	"LO Frequency [Hz]",	H5::PredType::IEEE_F32LE,	&LimeCfg.frq,		1},
		{"rlp",	"RX LowPass BW [Hz]",	H5::PredType::IEEE_F32LE,	&LimeCfg.RX_LPF,	1},
		{"tlp",	"TX LowPass BW [Hz]",	H5::PredType::IEEE_F32LE,	&LimeCfg.TX_LPF,	1},
		{"rgn",	"RX Gain [dB]",		H5::PredType::NATIVE_INT,	&LimeCfg.RX_gain,	1},
		{"tgn",	"TX Gain [dB]",		H5::PredType::NATIVE_INT,	&LimeCfg.TX_gain,	1},
		{"///",	"RX Gain readback [dB]",H5::PredType::NATIVE_INT,	&LimeCfg.RX_gain_rback,	4},
		{"///",	"TX Gain readback [dB]",H5::PredType::NATIVE_INT,	&LimeCfg.TX_gain_rback,	3},
		{"tdq",	"TX DC-correction Q",	H5::PredType::NATIVE_INT,	&LimeCfg.TX_QcorrDC,	1},
		{"tdi",	"TX DC-correction I",	H5::PredType::NATIVE_INT,	&LimeCfg.TX_IcorrDC,	1},
		{"tgi",	"TX I Gain correction",	H5::PredType::NATIVE_INT,	&LimeCfg.TX_IcorrGain,	1},
		{"tgq",	"TX Q Gain correction",	H5::PredType::NATIVE_INT,	&LimeCfg.TX_QcorrGain,	1},
		{"tpc",	"TX Phase correction",	H5::PredType::NATIVE_INT,	&LimeCfg.TX_IQcorrPhase,1},
		{"rgi",	"RX I Gain correction",	H5::PredType::NATIVE_INT,	&LimeCfg.RX_IcorrGain,	1},
		{"rgq",	"RX Q Gain correction",	H5::PredType::NATIVE_INT,	&LimeCfg.RX_QcorrGain,	1},
		{"rpc",	"RX Phase correction",	H5::PredType::NATIVE_INT,	&LimeCfg.RX_IQcorrPhase,1},
		{"npu",	"Number of Pulses",	H5::PredType::NATIVE_INT,	&LimeCfg.Npulses,	1},
		{"pdr",	"Pulse Duration [s]",	H5::PredType::IEEE_F64LE,	LimeCfg.p_dur,		(hsize_t) LimeCfg.Npulses},
		{"pof",	"Pulse Offset [Sa]",	H5::PredType::NATIVE_INT,	LimeCfg.p_offs,		(hsize_t) LimeCfg.Npulses},
		{"pam",	"IF Pulse Amplitude",	H5::PredType::IEEE_F64LE,	LimeCfg.p_amp,		(hsize_t) LimeCfg.Npulses},
		{"pfr",	"IF Pulse Frequency [Hz]",H5::PredType::IEEE_F64LE,	LimeCfg.p_frq,		(hsize_t) LimeCfg.Npulses},
		{"pph",	"IF Pulse Phase",	H5::PredType::IEEE_F64LE,	LimeCfg.p_pha,		(hsize_t) LimeCfg.Npulses},
		{"pcn",	"Nmbr of Phasecycles",	H5::PredType::NATIVE_INT,	LimeCfg.p_phacyc_N,	(hsize_t) LimeCfg.Npulses},
		{"pcl",	"Level of Phasecycle",	H5::PredType::NATIVE_INT,	LimeCfg.p_phacyc_lev,	(hsize_t) LimeCfg.Npulses},
		{"///",	"Pulse Duration [Sa]",	H5::PredType::NATIVE_INT,	LimeCfg.p_dur_smp,	(hsize_t) LimeCfg.Npulses},
		{"///",	"IF Pulse Frequency [1/Sa]",H5::PredType::IEEE_F64LE,	LimeCfg.p_frq_smp,	(hsize_t) LimeCfg.Npulses},
		{"amf",	"AM Frequency [Hz]",	H5::PredType::IEEE_F64LE,	LimeCfg.am_frq,		(hsize_t) LimeCfg.Npulses},
		{"amp",	"AM Phase [rad]",	H5::PredType::IEEE_F64LE,	LimeCfg.am_pha,		(hsize_t) LimeCfg.Npulses},
		{"amd",	"AM Depth",		H5::PredType::IEEE_F64LE,	LimeCfg.am_depth,	(hsize_t) LimeCfg.Npulses},
		{"amm",	"AM Mode",		H5::PredType::NATIVE_INT,	LimeCfg.am_mode,	(hsize_t) LimeCfg.Npulses},
		{"///",	"AM Frequency [1/Sa]",	H5::PredType::IEEE_F64LE,	LimeCfg.am_frq_smp,	(hsize_t) LimeCfg.Npulses},
		{"fmf",	"FM Frequency [Hz]",	H5::PredType::IEEE_F64LE,	LimeCfg.fm_frq,		(hsize_t) LimeCfg.Npulses},
		{"fmp",	"FM Phase [rad]",	H5::PredType::IEEE_F64LE,	LimeCfg.fm_pha,		(hsize_t) LimeCfg.Npulses},
		{"fmw",	"FM width [Hz]",	H5::PredType::IEEE_F64LE,	LimeCfg.fm_width,	(hsize_t) LimeCfg.Npulses},
		{"fmm",	"FM Mode",		H5::PredType::NATIVE_INT,	LimeCfg.fm_mode,	(hsize_t) LimeCfg.Npulses},
		{"///",	"FM Frequency [1/Sa]",	H5::PredType::IEEE_F64LE,	LimeCfg.fm_frq_smp,	(hsize_t) LimeCfg.Npulses},
		{"t0d",	"Trigger0 Timing [Sa]", H5::PredType::NATIVE_INT,	&LimeCfg.c0_tim,	4},
		{"t1d",	"Trigger1 Timing [Sa]", H5::PredType::NATIVE_INT,	&LimeCfg.c1_tim,	4},
		{"t2d",	"Trigger2 Timing [Sa]", H5::PredType::NATIVE_INT,	&LimeCfg.c2_tim,	4},
		{"t3d",	"Trigger3 Timing [Sa]", H5::PredType::NATIVE_INT,	&LimeCfg.c3_tim,	4},
		{"t0s",	"Trigger0 Synth [Sa]", 	H5::PredType::NATIVE_INT,	&LimeCfg.c0_synth,	5},
		{"t1s",	"Trigger1 Synth [Sa]", 	H5::PredType::NATIVE_INT,	&LimeCfg.c1_synth,	5},
		{"t2s",	"Trigger2 Synth [Sa]", 	H5::PredType::NATIVE_INT,	&LimeCfg.c2_synth,	5},
		{"t3s",	"Trigger3 Synth [Sa]", 	H5::PredType::NATIVE_INT,	&LimeCfg.c3_synth,	5},
		{"t0p",	"Trigger0 Enable",	H5::PredType::NATIVE_INT,	LimeCfg.p_c0_en,	(hsize_t) LimeCfg.Npulses},
		{"t1p",	"Trigger1 Enable",	H5::PredType::NATIVE_INT,	LimeCfg.p_c1_en,	(hsize_t) LimeCfg.Npulses},
		{"t2p",	"Trigger2 Enable",	H5::PredType::NATIVE_INT,	LimeCfg.p_c2_en,	(hsize_t) LimeCfg.Npulses},
		{"t3p",	"Trigger3 Enable",	H5::PredType::NATIVE_INT,	LimeCfg.p_c3_en,	(hsize_t) LimeCfg.Npulses},
		{"nrp",	"Nmbr of Repetitions",	H5::PredType::NATIVE_INT,	&LimeCfg.repetitions,	1},
		{"nav",	"Nmbr of Averages",	H5::PredType::NATIVE_INT,	&LimeCfg.averages,	1},
		{"trp",	"Repetition Time [s]",	H5::PredType::IEEE_F64LE,	&LimeCfg.reptime_secs,	1},
		{"tac",	"Acquisition Time [s]", H5::PredType::IEEE_F64LE,	&LimeCfg.rectime_secs,	1},
		{"///",	"Repetition Time [Sa]",	H5::PredType::NATIVE_INT,	&LimeCfg.reptime_smps,	1},
		{"///",	"Acquisition Time [Sa]",H5::PredType::NATIVE_INT,	&LimeCfg.rectime_smps,	1},
		{"bsz",	"Buffersize",		H5::PredType::NATIVE_INT,	&LimeCfg.buffersize,	1},
		{"pba",	"Pcyc before Avg if >0",H5::PredType::NATIVE_INT,	&LimeCfg.pcyc_bef_avg,	1},
		{"fpa",	"Filename Pattern",	H5::StrType(H5::PredType::C_S1, LimeCfg.file_pattern.length()+1),	(void *) LimeCfg.file_pattern.c_str(),	1},
		{"spt",	"Save Path",		H5::StrType(H5::PredType::C_S1, LimeCfg.save_path.length()+1),	(void *) LimeCfg.save_path.c_str(),	1},
		{"nos",	"Don't save if >0",	H5::PredType::NATIVE_INT,	&LimeCfg.override_save,	1},
		{"noi",	"Don't init if >0",	H5::PredType::NATIVE_INT,	&LimeCfg.override_init,	1},
		{"fst",	"Filename Timestamp",	H5::StrType(H5::PredType::C_S1, LimeCfg.file_stamp.length()+1),	(void *) LimeCfg.file_stamp.c_str(),	1},
		{"///",	"Exp Start Timestamp",	H5::StrType(H5::PredType::C_S1, LimeCfg.stamp_start.length()+1),	(void *) LimeCfg.stamp_start.c_str(),	1},
		{"///",	"Exp End Timestamp",	H5::StrType(H5::PredType::C_S1, LimeCfg.stamp_end.length()+1),	(void *) LimeCfg.stamp_end.c_str(),	1}
	};
	int no_of_attr = sizeof(HDFattr)/sizeof(Config2HDFattr_t);

	// iterate through arguments to parse eventual user input
	// (exposing the actual content of the struct to python would be nicer...)
	bool parse_prob = false;
	int curr_attr = -1;
	int curr_attr_last = -1;
	int attr2read = 0;
	int attr2read_last = 0;
	int attr_read = 0;
	for (int ii_arg = 1; ii_arg < argc; ii_arg++) {

		// get the attribute for the argument based on '-' (which also is there for negative numbers..)
		if (argv[ii_arg][0] == '-') {

			if ((strlen(argv[ii_arg]+1) != 3) && (attr2read == 0)) {
				cout << "Invalid argument "<< ii_arg <<": " << argv[ii_arg] << endl;
				parse_prob = true;
				continue;
			}
			// find matching attribute
			curr_attr_last = curr_attr;
			attr2read_last = attr2read;
			curr_attr = -1;
			for (int ii_attr = 0; ii_attr < no_of_attr; ii_attr++) {
				if (strcmp(argv[ii_arg]+1, HDFattr[ii_attr].arg.c_str()) == 0) {
					curr_attr = ii_attr;
					attr2read = HDFattr[ii_attr].dim;
					attr_read = 0;
					cout << "Found argument " << HDFattr[curr_attr].arg << ": " << HDFattr[curr_attr].Name << endl;
				}
			}
			// found nothing
			if (curr_attr == -1 && attr2read_last == 0) {
				cout << "Could not find valid attribute for argument "<< ii_arg <<": " << argv[ii_arg] << endl;
				parse_prob = true;
			// found something, but did not read the previous arguments
			} else if (curr_attr > -1 && attr2read_last > 0) {
				cout << "Missing argument: "<< attr2read_last <<" value missing for argument " << HDFattr[curr_attr_last].arg << endl;
				parse_prob = true;
			}
			// found nothing and did not read the previous arguments: a negative number
			if (curr_attr == -1 && attr2read_last > 0) {
				// restore the attribute and it as number
				curr_attr = curr_attr_last; 
				attr2read = attr2read_last;
			} else
				// all other cases: jump to the next argument
				continue;
		}

		// parse the value from the current attribute
		if (curr_attr != -1 && attr2read != 0) {

			// differentiate between the different types of input based on the H5::DataType
			// float values
			if (HDFattr[curr_attr].dType == H5::PredType::IEEE_F32LE) {
				*((float *) HDFattr[curr_attr].Value+attr_read) = atof(argv[ii_arg]);
				attr2read--; attr_read++;
				//cout << "Got value " << atof(argv[ii_arg]) << " from " << argv[ii_arg] << endl;
			}
			// double values
			if (HDFattr[curr_attr].dType == H5::PredType::IEEE_F64LE) {
				*((double *) HDFattr[curr_attr].Value+attr_read) = (double) atof(argv[ii_arg]);
				attr2read--; attr_read++;
				//cout << "Got value " << (double) atof(argv[ii_arg]) << " from " << argv[ii_arg] << endl;
			}
			// integer values
			if (HDFattr[curr_attr].dType == H5::PredType::NATIVE_INT) {
				*((int *) HDFattr[curr_attr].Value+attr_read) = atoi(argv[ii_arg]);
				attr2read--; attr_read++;
				//cout << "Got value " << atoi(argv[ii_arg]) << " from " << argv[ii_arg] << endl;
			}
			// strings: stored as std::string in LimeCfg and as Cstring in HDFattr.. 
			// --> explicitly treat strings, these are anyhow just a few for file/path info
			if (strcmp(HDFattr[curr_attr].arg.c_str(), "spt") == 0) {
				LimeCfg.save_path = argv[ii_arg];
				HDFattr[curr_attr].dType = H5::StrType(H5::PredType::C_S1, LimeCfg.save_path.length()+1);
				HDFattr[curr_attr].Value = (void *) LimeCfg.save_path.c_str();
				attr2read--; attr_read++;
			}
			if (strcmp(HDFattr[curr_attr].arg.c_str(), "fpa") == 0) {
				LimeCfg.file_pattern = argv[ii_arg];
				HDFattr[curr_attr].dType = H5::StrType(H5::PredType::C_S1, LimeCfg.file_pattern.length()+1);
				HDFattr[curr_attr].Value = (void *) LimeCfg.file_pattern.c_str();
				attr2read--; attr_read++;
			}
			if (strcmp(HDFattr[curr_attr].arg.c_str(), "fst") == 0) {
				LimeCfg.file_stamp = argv[ii_arg];
				HDFattr[curr_attr].dType = H5::StrType(H5::PredType::C_S1, LimeCfg.file_stamp.length()+1);
				HDFattr[curr_attr].Value = (void *) LimeCfg.file_stamp.c_str();
				attr2read--; attr_read++;
			}
		} else if (attr2read == 0) {
			cout << "Problem with argument " << HDFattr[curr_attr].arg << ": There is an input that is not clear, probably one input more than required! " << endl;
			parse_prob = true;
		}
	}
	// check if the last argument had all the values
	if (attr2read > 0) {
		cout << "Missing argument: "<< attr2read <<" value missing for argument " << HDFattr[curr_attr].arg << endl;
		parse_prob = true;
	}
	if (parse_prob) {
		cout << "Exiting due to problem with provided arguments! Valid arguments are (exept -///, which cannot be set by the user):" << endl;
		string datatype;
		for (int ii_attr = 0; ii_attr < no_of_attr; ii_attr++) {

			// get the datatype
			if (HDFattr[ii_attr].dType == H5::PredType::IEEE_F32LE) datatype = "float";
			else if (HDFattr[ii_attr].dType == H5::PredType::IEEE_F64LE) datatype = "double";
			else if (HDFattr[ii_attr].dType == H5::PredType::NATIVE_INT) datatype = "int";
			else datatype = "string";
			cout << "-" << HDFattr[ii_attr].arg << "   " << left << setw(30) << HDFattr[ii_attr].Name << ": " << HDFattr[ii_attr].dim << "x " << datatype << endl;

		}
		return 1;
	}


	// convert input in seconds/Hz to samples
	for (int ii = 0; ii < LimeCfg.Npulses; ii++) {
		LimeCfg.p_dur_smp[ii] = round(LimeCfg.p_dur[ii] * LimeCfg.srate);
		LimeCfg.p_frq_smp[ii] = LimeCfg.p_frq[ii] / LimeCfg.srate;
		LimeCfg.am_frq_smp[ii] = LimeCfg.am_frq[ii] / LimeCfg.srate;
		LimeCfg.fm_frq_smp[ii] = LimeCfg.fm_frq[ii] / LimeCfg.srate;
	}


	// check directory first
	if (makePath(LimeCfg.save_path) == 0) { 
		cout << "Problem entering the specified path: " << LimeCfg.save_path << endl;
		return 1;
	}


	//Find devices
	int n;
	lms_info_str_t list[8]; //should be large enough to hold all detected devices

	if ((n = LMS_GetDeviceList(list)) < 0) //NULL can be passed to only get number of devices
		error();

	cout << "Devices found: " << n << endl; //print number of devices
	if (n < 1) return -1;

	//open the first device
	if (LMS_Open(&device, list[n-1], NULL)) error();

/*
	//print available antennae names
	//select antenna port
	lms_name_t antenna_list[10];    //large enough list for antenna names.
	//Alternatively, NULL can be passed to LMS_GetAntennaList() to obtain number of antennae
	if ((n = LMS_GetAntennaList(device, LMS_CH_RX, 0, antenna_list)) < 0) error();

	// get and print antenna index and name
	if ((n = LMS_GetAntenna(device, LMS_CH_RX, 0)) < 0) error();
	cout << "Automatically selected RX LNA: " << n << ": " << antenna_list[n] << endl;
*/

	//Get number of channels
	if ((n = LMS_GetNumChannels(device, LMS_CH_RX)) < 0) error();
	cout << "Number of RX channels: " << n << endl;
	if ((n = LMS_GetNumChannels(device, LMS_CH_TX)) < 0) error();
	cout << "Number of TX channels: " << n << endl;


	// check if the settings are already there
	float_type frq_read;
	if (LMS_GetLOFrequency(device, LMS_CH_RX, 0, &frq_read) != 0) error(); 

	float_type srate_read, rf_rate;
	if (LMS_GetSampleRate(device, LMS_CH_RX, 0, &srate_read, &rf_rate) != 0) error();

	bool frqdev = fabs(frq_read - LimeCfg.frq) > 1.0;
	bool sratedev = fabs(srate_read - LimeCfg.srate) > 1.0;


	// Getting the gain
	int RXgain[4];	
	int TXgain[3];
	GetGainRXTX(RXgain, TXgain);

	bool rgndev = RXgain[0] != LimeCfg.RX_gain;
	bool tgndev = TXgain[0] != LimeCfg.TX_gain;
	if (TXgain[0] > 55 && LimeCfg.TX_gain > 55) {
		tgndev = false;
		cout << "Unable to check for variation in TXgain setting, since it is impossible to retrieve it for TXgain > 55 dB without altering the RF performance. Eventual changes in the TXgain are thus not taken into account." << endl;
	}
	
	/*
	// Similar as with the built in GetGaindB function, the GetLPFBW function is also affecting the actual reading of the LPF. It is actually not entirely clear why this happens, as compared to the GetGaindB function, where it is evident that some calibration is done..
	// Accordingly, one must take care that the LPFBW is set right at the beginning when opening the device
	float_type LPFBW, LPFBW2; // lowpass bandwidth
	if (LMS_GetLPFBW(device, LMS_CH_RX, 0, &LPFBW) != 0) error();
	bool rlpfdev = LPFBW != LimeCfg.RX_LPF;
	if (LMS_GetLPFBW(device, LMS_CH_TX, 0, &LPFBW2) != 0) error();
	bool tlpfdev = LPFBW2 != LimeCfg.TX_LPF;
	*/


	// initialize LimeSDR if there is a deviation in relevant parameters or if it is enforced to init, not init
	//if (frqdev || sratedev || tgndev || rgndev || rlpfdev || tlpfdev || true) {
	bool override_init = LimeCfg.override_init > 0; // override the initialization if -noi > 0
	bool enforce_init = LimeCfg.override_init < 0; // enforce init if -noi < 0
	
	if ( ((frqdev || sratedev || tgndev || rgndev ) && !override_init) || enforce_init ) {
		
		// just to re-assure why there is another setup
		cout << "Re-initialization of parameters ... " << endl;
		if (frqdev) cout << "... due to LOfrequency deviation by " << frq_read - LimeCfg.frq << " from " << LimeCfg.frq << endl;
		if (sratedev) cout << "... due to samplerate deviation by " << srate_read - LimeCfg.srate << " from " << LimeCfg.srate << endl;
		if (rgndev) cout << "... due to RX gain deviation by " << RXgain[0] - LimeCfg.RX_gain << " from " << LimeCfg.RX_gain << endl;
		if (tgndev) cout << "... due to TX gain deviation by " << TXgain[0] - LimeCfg.TX_gain << " from " << LimeCfg.TX_gain << endl;
		//if (rlpfdev) cout << "... due to RX LPF deviation by " << LPFBW - LimeCfg.RX_LPF << " from " << LimeCfg.RX_LPF << endl;
		//if (tlpfdev) cout << "... due to TX LPF deviation by " << LPFBW2 - LimeCfg.TX_LPF << " from " << LimeCfg.TX_LPF << endl;

		// First mute the TX output, as the init commands create a lot of garbage
		if (LMS_WriteParam(device, LMS7_PD_TLOBUF_TRF, 1) != 0) error();
		if (LMS_SetGaindB(device, LMS_CH_TX, 0, 0)!= 0) {

			cout << "Initializing device first!" << endl;

			// this might fail for a freshly connected device
			// --> init the device
			if (LMS_Init(device) != 0) error();
			// retry
			if (LMS_SetGaindB(device, LMS_CH_TX, 0, 0) != 0) error();
		}
		if (LMS_SetNormalizedGain(device, LMS_CH_TX, 0, 0.0) != 0) error();

		//Set RX center frequency
		if (LMS_SetLOFrequency(device, LMS_CH_RX, 0, LimeCfg.frq) != 0) error(); 

		//Set TX center frequency
		if (LMS_SetLOFrequency(device, LMS_CH_TX, 0, LimeCfg.frq) != 0) error();

		// Read back the updated frequency for later storage
		if (LMS_GetLOFrequency(device, LMS_CH_RX, 0, &frq_read) != 0) error(); 

		//Enable RX channel
		//Channels are numbered starting at 0
		if (LMS_EnableChannel(device, LMS_CH_RX, 0, true) != 0) error();
		//Enable TX channels
		if (LMS_EnableChannel(device, LMS_CH_TX, 0, true) != 0) error();


		// apply DC offset in TxTSP
		uint16_t DC_I, DC_Q, DC_EN;
		DC_EN = 0;
		if (LMS_WriteParam(device, LMS7_DCCORRI_TXTSP, LimeCfg.TX_IcorrDC) != 0) error();
		if (LMS_WriteParam(device, LMS7_DCCORRQ_TXTSP, LimeCfg.TX_QcorrDC) != 0) error();
		if (LMS_WriteParam(device, LMS7_DC_BYP_TXTSP, DC_EN) != 0) error();


		if (LMS_WriteParam(device, LMS7_GCORRI_TXTSP, LimeCfg.TX_IcorrGain) != 0) error();
		if (LMS_WriteParam(device, LMS7_GCORRQ_TXTSP, LimeCfg.TX_QcorrGain) != 0) error();
		if (LMS_WriteParam(device, LMS7_IQCORR_TXTSP, LimeCfg.TX_IQcorrPhase) != 0) error();
		if (LMS_WriteParam(device, LMS7_GCORRI_RXTSP, LimeCfg.RX_IcorrGain) != 0) error();
		if (LMS_WriteParam(device, LMS7_GCORRQ_RXTSP, LimeCfg.RX_QcorrGain) != 0) error();
		if (LMS_WriteParam(device, LMS7_IQCORR_RXTSP, LimeCfg.RX_IQcorrPhase) != 0) error();

		//added by me as the IQ calibration did not happen on the chip from python or c++
		if (LMS_WriteParam(device, LMS7_MAC, 1) != 0) error();
		/*
		// read back DC offset in TxTSP
		if (LMS_ReadParam(device, LMS7_DCCORRI_TXTSP, &DC_I) != 0) error();
		if (LMS_ReadParam(device, LMS7_DCCORRQ_TXTSP, &DC_Q) != 0) error();
		if (LMS_ReadParam(device, LMS7_DC_BYP_TXTSP, &DC_EN) != 0) error();
		cout << "TxTSP DC corr (EN, I, Q): " << DC_EN << ", " << DC_I << ", " <<  DC_Q << endl;           
		*/


		//print available antennae names
		//select antenna port
		lms_name_t antenna_list[10];    //large enough list for antenna names.
		//Alternatively, NULL can be passed to LMS_GetAntennaList() to obtain number of antennae
		if ((n = LMS_GetAntennaList(device, LMS_CH_RX, 0, antenna_list)) < 0) error();

		cout << "Available RX LNAs:\n";            //print available antennae names
		for (int i = 0; i < n; i++)
			cout << i << ": " << antenna_list[i] << endl;
		// get and print antenna index and name
		if ((n = LMS_GetAntenna(device, LMS_CH_RX, 0)) < 0) error();
		cout << "Automatically selected RX LNA: " << n << ": " << antenna_list[n] << endl;

		// manually select antenna
		if (LMS_SetAntenna(device, LMS_CH_RX, 0, LMS_PATH_LNAL) != 0) error();

		// get and print antenna index and name
		if ((n = LMS_GetAntenna(device, LMS_CH_RX, 0)) < 0) error();
		cout << "Manually selected RX LNA: " << n << ": " << antenna_list[n] << endl;

		//select antenna port
		//Alternatively, NULL can be passed to LMS_GetAntennaList() to obtain number of antennae
		if ((n = LMS_GetAntennaList(device, LMS_CH_TX, 0, antenna_list)) < 0) error();

		cout << "Available TX pathways:\n";            //print available antennae names
		for (int i = 0; i < n; i++)
			cout << i << ": " << antenna_list[i] << endl;

		// get and print print antenna index and name
		if ((n = LMS_GetAntenna(device, LMS_CH_TX, 0)) < 0) 
			error();
		cout << "Automatically selected TX pathway: " << n << ": " << antenna_list[n] << endl;

 		// manually select antenna
		int mychoice = LMS_PATH_TX1;
		if (LimeCfg.frq > 1500e6) mychoice = LMS_PATH_TX2;
		mychoice = LMS_PATH_TX1; // HACK: hardcode TX2 pathway
		if (LMS_SetAntenna(device, LMS_CH_TX, 0, mychoice) != 0) error();

		// get and print print antenna index and name
		if ((n = LMS_GetAntenna(device, LMS_CH_TX, 0)) < 0) error();
		cout << "Manually selected TX pathway: " << n << ": " << antenna_list[n] << endl;

		// Set sample rate, w/o oversampling, so that we can remove the invsinc filter
		if (LMS_SetSampleRate(device, LimeCfg.srate, 1) != 0) error();
		// Invsinc, which removes that non-causal wiggle in timedomain
		if (LMS_WriteParam(device, LMS7_ISINC_BYP_TXTSP, 1) != 0) error();
		// CMIX: Disable, as it is not used
		if (LMS_WriteParam(device, LMS7_CMIX_BYP_TXTSP, 1) != 0) error();
		if (LMS_WriteParam(device, LMS7_CMIX_BYP_RXTSP, 1) != 0) error();

		// experiment with the GFIR filters
		// if (LMS_SetGFIRLPF(device, LMS_CH_RX, 0, 1, 0.5e6) != 0) error(); // Works nicely. Allows, for instance, to perform narrowband observation together with CMIX


		// Remute the TX output here, as the init commands create a lot of garbage
		if (LMS_WriteParam(device, LMS7_PD_TLOBUF_TRF, 1) != 0) error();

		// Set RX and TX to the gain values
		if (LMS_SetGaindB(device, LMS_CH_TX, 0, LimeCfg.TX_gain) != 0) error();
		if (LMS_SetGaindB(device, LMS_CH_RX, 0, LimeCfg.RX_gain) != 0) error();

		cout << "After gain setting: " << endl;
		GetGainRXTX(RXgain, TXgain);

		// special for low frequency operation: LNA gain saturates rather early -> reduce lna gain and increase pga
		// ( and even though we have that function GetGainRXTX(), we need to re-read the values here explicitly, since
		//   we need to operate on the actual settings of the LMS Parameter, and not the gain values )
		uint16_t gain_lna, gain_tia, gain_pga;
		if (LMS_ReadParam(device, LMS7_G_LNA_RFE, &gain_lna) != 0) error();
		if (LMS_ReadParam(device, LMS7_G_TIA_RFE, &gain_tia) != 0) error();
		if (LMS_ReadParam(device, LMS7_G_PGA_RBB, &gain_pga) != 0) error();
		// cout << "Indiv gain addr: " << gain_lna << " LNA, " << gain_tia << " TIA, " << gain_pga << " PGA" << endl;
		// gain_lna > 7 means a gain beyond gmax-12. Convert that to gains in dB
		uint16_t crit_val = 7;
		uint16_t gain_corr = (gain_lna - crit_val);
		if (gain_corr > 2) gain_corr += 4; // gain steps of 1 dB for gain_lna > 9
		else gain_corr *= 3; // gain steps of 3 dB for gain_lna <= 9
		// eventually put this to the pga gain
		if (gain_corr > 0) {
			if (LMS_WriteParam(device, LMS7_G_LNA_RFE, crit_val) != 0) error();
			if (LMS_WriteParam(device, LMS7_G_PGA_RBB, gain_pga + gain_corr) != 0) error();
		}
		GetGainRXTX(RXgain, TXgain);

		//Get allowed LPF bandwidth range
		lms_range_t range;
		if (LMS_GetLPFBWRange(device,LMS_CH_RX,&range)!=0) error();
		cout << "RX LPF bandwitdh range: " << range.min / 1e6 << " - " << range.max / 1e6 << " MHz\n\n";

		if (LMS_GetLPFBWRange(device,LMS_CH_TX,&range)!=0) error();
		cout << "TX LPF bandwitdh range: " << range.min / 1e6 << " - " << range.max / 1e6 << " MHz\n\n";

		if (LMS_SetLPFBW(device,LMS_CH_RX,0, LimeCfg.RX_LPF)!=0) error();
		if (LMS_SetLPFBW(device,LMS_CH_TX,0, LimeCfg.TX_LPF)!=0) error();


		float_type LPFBW; // lowpass bandwidth
		if (LMS_GetLPFBW(device, LMS_CH_RX, 0, &LPFBW) != 0) error();
		cout << "RX LPFBW: " << LPFBW/1e6 << " MHz" << endl;
		if (LMS_GetLPFBW(device, LMS_CH_TX, 0, &LPFBW) != 0) error();
		cout << "TX LPFBW: " << LPFBW/1e6 << " MHz" << endl;

		// Set limelight interface to TRXIQ, as the std value (JESD) will not communicate
		if (LMS_WriteParam(device, LMS7_LML1_MODE, 0) != 0) error();
		if (LMS_WriteParam(device, LMS7_LML2_MODE, 0) != 0) error();

		// Unmute the TX output, as the init commands are now written
		if (LMS_WriteParam(device, LMS7_PD_TLOBUF_TRF, 0) != 0) error();

	}

	// read back values that tend to depend on the specific configuration
	memcpy(LimeCfg.TX_gain_rback, TXgain, 3* sizeof *LimeCfg.TX_gain_rback);
	memcpy(LimeCfg.RX_gain_rback, RXgain, 4* sizeof *LimeCfg.RX_gain_rback);


	const int chCount = 1; //number of RX/TX streams

	// Initialize acquisition data buffer
	int buffersize = LimeCfg.buffersize; //complex samples per buffer
	// note that proper scheduling requires buffersize that is a multiple of 1360 (12bit RX) and 1020 (16bit TX)
	// accordingly, buffersize needs to be a multiple of 4080, which is 3*1360 and 4*1020
	if (buffersize % 4080 != 0) {

		cout << "Problem with requested buffersize of " << LimeCfg.buffersize << ", as it is not a multiple of 4080." << endl;
		LMS_Close(device);
		return 1;

	}


	int timestampOffset = 0; 	// for offsets between TX and RX timestamps
	int bufferOffset = 0; 		// to correct for those offsets
	int16_t * buffers[chCount];
	for (int ii = 0; ii < chCount; ++ii)
	{
		buffers[ii] = new int16_t[buffersize * 2]; //buffer to hold complex values (2*samples)
	}

	//Streaming Setup
	lms_stream_t rx_streams[chCount];
	lms_stream_t tx_streams[chCount];

	int N_buffers_per_fifo = 96; // Number of buffers that can be put onto the fifo

	//Initialize streams
	//All streams setups should be done before starting streams. New streams cannot be set-up if at least stream is running.
	for (int ii = 0; ii < chCount; ++ii)
	{
		rx_streams[ii].channel = ii; //channel number
		rx_streams[ii].fifoSize = buffersize * N_buffers_per_fifo; //fifo size in samples
		rx_streams[ii].throughputVsLatency = 1.0; //1.0 max throuhput, 0.0 min latency
		rx_streams[ii].isTx = false; //RX channel
		rx_streams[ii].dataFmt = lms_stream_t::LMS_FMT_I12; //12-bit integers

		if (LMS_SetupStream(device, &rx_streams[ii]) != 0) error();

		tx_streams[ii].channel = ii; //channel number
		tx_streams[ii].fifoSize = buffersize * N_buffers_per_fifo; //fifo size in samples
		tx_streams[ii].throughputVsLatency = 1.0; //1.0 max throuhput, 0.0 min latency
		tx_streams[ii].isTx = true; //TX channel
		tx_streams[ii].dataFmt = lms_stream_t::LMS_FMT_I16; //16-bit float

		if (LMS_SetupStream(device, &tx_streams[ii]) != 0) error();
	}


	//gather parameters for the TX pulse 

	// first get all the phase-cycles
	// which at first requires few maximum quantities....
	// .... the number of levels ...
	int max_lev = 0;
	for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) if (LimeCfg.p_phacyc_lev[ii_pls] > max_lev) max_lev = LimeCfg.p_phacyc_lev[ii_pls];

	// check if there are no gaps in the level specification
	bool found_level[max_lev+1];
	bool level_problem = false;
	for (int ii = 0; ii < max_lev + 1; ii++) {
		found_level[ii] = false;
		for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) if (LimeCfg.p_phacyc_lev[ii_pls] == ii) found_level[ii] = true;
		if (!found_level[ii]) level_problem = true;
	}
	if (level_problem) {
		cout << "Problem with specified phase cycle levels: ";
		for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) cout << setw(5) << left << LimeCfg.p_phacyc_lev[ii_pls];
		cout << endl;
		cout << "A consecutive level numbering is required, but level/s ";
		for (int ii = 0; ii < max_lev + 1; ii++) if (!found_level[ii]) cout << setw(2) << left << ii;
		cout << " is/are missing!" << endl;

		LMS_Close(device);
		return 1;
	}
	// ... the maximum number of phase cycles per level ...
	int * steps_per_lev = new int[max_lev + 1];
	for (int ii = 0; ii < max_lev + 1; ii++) steps_per_lev[ii] = 0;

	int curr_lev_steps; // to make the code more readable...
	for (int ii = 0; ii < LimeCfg.Npulses; ii++) {
		curr_lev_steps = steps_per_lev[LimeCfg.p_phacyc_lev[ii]];
		if (LimeCfg.p_phacyc_N[ii] > curr_lev_steps)  steps_per_lev[LimeCfg.p_phacyc_lev[ii]] = LimeCfg.p_phacyc_N[ii];
	}

	// ... which gives the total number of phase variations ...
	int num_phavar = 1;
	int steps_incr[max_lev + 1] = {1}; // .. and the number of steps where phase is constant ...
	for (int ii = 0; ii < max_lev + 1; ii++) {
		if (ii > 0) steps_incr[ii] = steps_incr[ii-1] * steps_per_lev[ii-1];
		num_phavar *= steps_per_lev[ii];
	}
	if (num_phavar < 1) {
			cout << "Problem with specified number of phases (pcn) for pulses 0 to " << LimeCfg.Npulses-1 << ": " << endl;
			for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) cout << setw(5) << left <<LimeCfg.p_phacyc_N[ii_pls];
			cout << endl;
			cout << "Number of pulse phases must be >0 for pulses:";
			for (int ii = 0; ii < LimeCfg.Npulses; ii++) if (LimeCfg.p_phacyc_N[ii] < 1) cout << setw(2) << left << ii;
			cout << endl;

			LMS_Close(device);
			return 1;
	}

	// ... which allows to construct the entire phase table ...
	double pha_tab[num_phavar][LimeCfg.Npulses];

	double pha_incr, curr_pha; 
	int step_incr = 1; 

	for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) {
		// retrieve the phase increment
		if (LimeCfg.p_phacyc_N[ii_pls] != 0)
			pha_incr = 1.0/LimeCfg.p_phacyc_N[ii_pls];
		else 
			pha_incr = 1.0;

		curr_pha = 0;

		// get the step increment
		step_incr = steps_incr[LimeCfg.p_phacyc_lev[ii_pls]];

		// start to fill the table
		for (int ii_pha = 0; ii_pha < num_phavar; ii_pha++) { 
			// eventually increment the phase
			if ((ii_pha > 0) && (ii_pha % step_incr == 0)) curr_pha += pha_incr;

			pha_tab[ii_pha][ii_pls] = fmod(curr_pha, 1.0);
		}
	}

	// debug: print that phase table
	cout << "Phase Table : " << endl;
	for (int ii_pha = 0; ii_pha < num_phavar; ii_pha++) { 
		for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) {
			cout << setw(10) << left << pha_tab[ii_pha][ii_pls];
		}
		cout << endl;
	}


	// get the number of buffers that are required in order to fit the entire experiment
	long exc_len = 0;
	int exc_buffers;
	int pulsedur, pulseoffs;
	pulseoffs = 0;
	for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) {

		pulsedur = LimeCfg.p_dur_smp[ii_pls];	// duration of pulse in samples
		pulseoffs += LimeCfg.p_offs[ii_pls];	// offset of pulse in samples

		if (pulseoffs + pulsedur > exc_len)
			exc_len = pulseoffs + pulsedur;
	}
	exc_buffers = ceil((double) exc_len / (double) buffersize);
	cout << "Excitation pattern: " << exc_len << " samples (" << exc_buffers << " buffers with " << buffersize << " samples each)" << endl;


	// TX buffers
	//int16_t tx_buffer[num_phavar][exc_buffers][2*buffersize];  	// buffer to hold complex values (2* samples), including phase cycles
	// TODO: put in the same way as the acq buffer, i.e. as an array of pointers. Otherwise, there is a limitation in space that can be used
	int16_t * tx_buffer[num_phavar][exc_buffers];
	for (int ii = 0; ii < num_phavar; ++ii) {
		for (int jj = 0; jj < exc_buffers; ++jj) {
			tx_buffer[ii][jj] = new int16_t[2*buffersize];
		}
	}
	int16_t tx_buffer_1st[2*buffersize];    	// buffer to hold complex values
	float 	fsmpI, fsmpQ;
	int16_t smpI, smpQ;

	// init with zero, as we add to it
	for (int ii = 0; ii < 2*buffersize; ii++) {
		for (int jj = 0; jj < exc_buffers; jj++) {
			for (int ll = 0; ll < num_phavar; ll++) tx_buffer[ll][jj][ii] = 0;
		}
	}
	

	// pulse parameters
	double pulsefrq, pulseamp, pulsepha, pulsepha_inst, pulseamp_inst;
	double w, w_mod, mlt_mod, pha_acc, fm_width_smp;
	int buffoffs;
	

	pulseoffs = 0;
	for (int ii_pls = 0; ii_pls < LimeCfg.Npulses; ii_pls++) {

		pulsedur = LimeCfg.p_dur_smp[ii_pls];	// duration of pulse in samples
		pulseoffs += LimeCfg.p_offs[ii_pls];	// offset of pulse in samples
		pulsefrq = LimeCfg.p_frq_smp[ii_pls];	// frequency of pulse in samples
		pulseamp = LimeCfg.p_amp[ii_pls];	// relative amplitude of pulses
		pulsepha = LimeCfg.p_pha[ii_pls];	// phase of pulse

		pha_acc = 0;				// phase accumulation under FM
		fm_width_smp = 2*pi*LimeCfg.fm_width[ii_pls] / LimeCfg.srate;	// width of FM in rad/sample for correct accumulation

		for (int ll = 0; ll < num_phavar; ll++) {      			// generate TX Pulse for different phases
			buffoffs = 0;
			for (int jj = 0; jj < exc_buffers; jj++) {		// distribute 'long experiment' amongst buffers
				for (int ii = 0; ii < buffersize; ii++) {      	// generate TX Pulse point by point
					if ((ii + buffoffs >= pulseoffs) & (ii + buffoffs < pulsedur + pulseoffs)) {

						//w = 2*pi*(ii+buffoffs-pulseoffs)*pulsefrq; // frequency*time, such that each pulse begins at zero phase

						w = 2*pi*(ii-pulseoffs)*pulsefrq;		// re-put absolute phase, which is better suited for pulsed experiments. The inclusion of buffoffs above was actually intended for CW type experiments, which were put separately in CW_AFC_engine.

						// instantaneous pulseamp/pha
						pulsepha_inst = pulsepha;
						pulseamp_inst = pulseamp;

						// implement AM
						if (LimeCfg.am_frq[ii_pls] != 0) {
							w_mod = 2*pi*(ii+buffoffs-pulseoffs)*LimeCfg.am_frq_smp[ii_pls]; // inst modphase
							mlt_mod = Modfunction(w_mod + LimeCfg.am_pha[ii_pls], LimeCfg.am_mode[ii_pls]);
							mlt_mod = ((mlt_mod - 1.0)*LimeCfg.am_depth[ii_pls])+1.0;
							pulseamp_inst = pulseamp*mlt_mod;
						}

						// implement FM, currently by implementing the corresponding phase integral analytically
						if (LimeCfg.fm_frq[ii_pls] != 0) {
							w_mod = 2*pi*(ii+buffoffs-pulseoffs)*LimeCfg.fm_frq_smp[ii_pls]; // inst modphase
							if (LimeCfg.fm_mode[ii_pls] == 0) {// cosine FM -> sine PM
								mlt_mod = Modfunction(w_mod + LimeCfg.fm_pha[ii_pls] - pi/2, LimeCfg.fm_mode[ii_pls]);
							}
							else if (LimeCfg.fm_mode[ii_pls] == 1) { // tirangluar FM --> quadratic PM
								mlt_mod = Modfunction(w_mod + LimeCfg.fm_pha[ii_pls] - pi/2, LimeCfg.fm_mode[ii_pls]);

							}
							else if (LimeCfg.fm_mode[ii_pls] == 2) {// square FM --> triangular PM
								mlt_mod = Modfunction(w_mod + LimeCfg.fm_pha[ii_pls] - pi/2, 1);

							}
							mlt_mod = LimeCfg.fm_width[ii_pls]/2 * mlt_mod / LimeCfg.fm_frq[ii_pls];
							pulsepha_inst = pulsepha+mlt_mod;

							if (LimeCfg.fm_mode[ii_pls] > 90) { // method with accumulator
								mlt_mod = Modfunction(w_mod + LimeCfg.fm_pha[ii_pls], LimeCfg.fm_mode[ii_pls]-100);
								mlt_mod = fm_width_smp/2 * mlt_mod;
								pha_acc += mlt_mod;
								pulsepha_inst = pulsepha+pha_acc;

							}
						}

						fsmpI = pulseamp_inst*cos(w+pulsepha_inst+2*pi*pha_tab[ll][ii_pls]);
						fsmpQ = pulseamp_inst*sin(w+pulsepha_inst+2*pi*pha_tab[ll][ii_pls]);

						// convert to int16 ... 
						smpI   = 2047.0 * fsmpI;	
						smpQ   = 2047.0 * fsmpQ;	

						// ... with 4 LSB at 0 for marker
						if (tx_streams[0].dataFmt == lms_stream_t::LMS_FMT_I16) {
							smpI 	= smpI << 4;	
							smpQ 	= smpQ << 4;	
						}
						// add to buffer
						tx_buffer[ll][jj][2*ii]   += smpI;	
						tx_buffer[ll][jj][2*ii+1] += smpQ;	
					} else {
						//fsmpI = 0.0;
						//fsmpQ = 0.0;
					}
				}
			buffoffs += buffersize; // jump to next buffer
			}
		}

		// Pulse Marker for timing relative to pulse flanks
		// TODO: we might need some gate joining and one should also warn if the triggers do not fit into the buffer
		if (tx_streams[0].dataFmt == lms_stream_t::LMS_FMT_I16) {
			int* curr_marker;
			int* curr_marker_en;
			// marker channel for that offset
			for (int ii_c = 0; ii_c <4; ii_c++) {      // iterate through the four marker channels
				// get the proper configuration of the trigger channel
				switch (ii_c) {
					case 0: curr_marker = LimeCfg.c0_tim; curr_marker_en = LimeCfg.p_c0_en; break;
					case 1: curr_marker = LimeCfg.c1_tim; curr_marker_en = LimeCfg.p_c1_en; break;
					case 2: curr_marker = LimeCfg.c2_tim; curr_marker_en = LimeCfg.p_c2_en; break;
					case 3: curr_marker = LimeCfg.c3_tim; curr_marker_en = LimeCfg.p_c3_en; break;
					default : break;
				}

				// check if the channel is activated
				if (curr_marker[0] == 0 || curr_marker_en[ii_pls] == 0) continue;

				// set trigger with bitset operation
				for (int ll = 0; ll < num_phavar; ll++) {   
					buffoffs = 0;
					for (int jj = 0; jj < exc_buffers; jj++) {		// distribute 'long experiment' amongst buffers
						for (int ii = 0; ii < 2*buffersize; ii++) {   	// set trigger point by point
							if ((ii + buffoffs >= 2*pulseoffs + curr_marker[2] - curr_marker[1]) & (ii + buffoffs < 2*pulsedur + 2*pulseoffs + curr_marker[2] + curr_marker[3])) {
								tx_buffer[ll][jj][ii] |=  1<<ii_c; 
							}
						}
						buffoffs += 2*buffersize; // jump to next buffer
					}
				}
			}
		}
	}


	// Synth Marker for CW sync stuff
	// Use TTL channel as synth: [enabled? , half-period, strt, PSK shift, PSK adv]
	int synthstart = 0;
	int wrapped_phase = 0;
	if (tx_streams[0].dataFmt == lms_stream_t::LMS_FMT_I16) {
		int* curr_synth;
		// marker channel for that offset
		for (int ii_c = 0; ii_c <4; ii_c++) {      // iterate through the four marker channels
			// get the proper configuration of the trigger channel
			switch (ii_c) {
				case 0: curr_synth = LimeCfg.c0_synth; break;
				case 1: curr_synth = LimeCfg.c1_synth; break;
				case 2: curr_synth = LimeCfg.c2_synth; break;
				case 3: curr_synth = LimeCfg.c3_synth; break;
				default : break;
			}

			// check if the channel is activated
			if (curr_synth[0] == 0) continue;


			cout << "TTL-synth t" << ii_c << " toggles state after " << curr_synth[1] << " samples" << endl;

			// set trigger with bitset operation
			synthstart = curr_synth[2];
			for (int ll = 0; ll < num_phavar; ll++) {   
				buffoffs = 0;

				// eventually advance the synth coupled to the phase cycle
				if (curr_synth[4] > 0) {
					if ((ll % curr_synth[4]) == 0)	synthstart += curr_synth[3];
				}

				for (int jj = 0; jj < exc_buffers; jj++) {		// distribute 'long experiment' amongst buffers
					for (int ii = 0; ii < 2*buffersize; ii++) {   	// set trigger point by point
						// wrap the phase counter
						wrapped_phase = int(int(ii + buffoffs + synthstart) % int(2 * curr_synth[1]));

						//wrapped_phase = 0;
						//test = (wrapped_phase < curr_synth[1]);
						if (wrapped_phase < curr_synth[1]) {
							tx_buffer[ll][jj][ii] |=  1<<ii_c; 
						}
					}
					buffoffs += 2*buffersize; // jump to next buffer
				}
			}
		}
	}

	//generate empty TX Pulse at beginning
	for (int ii = 0; ii <buffersize; ii++) { 

		tx_buffer_1st[2*ii] = 0.0;	
		tx_buffer_1st[2*ii+1] = 0.0;	
	}
 


	// calculate the repetition and recording time in samples as mutliple of buffer size
	// in this way, we do not need to do any exhaustive sample alignment strategies
	long rep_offset, rec_len;
	rep_offset = ceil(LimeCfg.reptime_secs * LimeCfg.srate / (double) buffersize) * buffersize;
	rec_len = ceil(LimeCfg.rectime_secs * LimeCfg.srate / (double) buffersize) * buffersize;

	// write back to LimeCfg so that these are stored in the file
	LimeCfg.reptime_smps = rep_offset;
	LimeCfg.rectime_smps = rec_len;

	if (rec_len > rep_offset) {
		cout << "Acquisition time of " << rec_len << " samples cannot be longer than repetition time (" << rep_offset << " Samples)" << endl;
		error();
	}	

	cout << "Repetition and acquisition times: " << rep_offset <<  " Sa (" << rep_offset/buffersize << " buffers), " << rec_len << " Sa (" << rec_len/buffersize << " buffers with " << buffersize << " Sa each)" << endl;


	// Buffer for acqisition signal: integer datatype, so that we can have a sufficient number of averages of acquired 16 bit data into the 32 bit buffer
	// for some reason, there are segfaults here when acqbuf_size becomes something on the order of 100
	int acqbuf_size = LimeCfg.repetitions * num_phavar;
	//int acqbuf[acqbuf_size][2*rec_len]; // causes segfaults with large arrays...

	// init as non-contiguous memory (which will require writing as chunks to HDF5)
	int * acqbuf[acqbuf_size];
	for (int ii = 0; ii < acqbuf_size; ++ii)
	{
		acqbuf[ii] = new int[2*rec_len];
	}
	
	// brute-force initialization by zero ( memset(acqbuf, 0, acqbuf_size*2*rec_len); ) did not work...
	for (int ii = 0; ii<acqbuf_size; ii++) {
		for (int jj = 0; jj<2*rec_len; jj++) {
			acqbuf[ii][jj] = 0 ;
		}
	}

	// mirror buffer: just holds a copy of the entire current record, without 32 to 16 bit conversion
	int16_t* mirror_buf;
	mirror_buf = new int16_t[2*rec_len];

	// number of lost data due to packet loss
	int lost[acqbuf_size] = {0}; 
	std::list<int> lost_acqs = {};

	
	//Streaming
	lms_stream_meta_t rx_metadata; 		//Use metadata for additional control over sample receive function behavior
	rx_metadata.flushPartialPacket = false; //currently has no effect in RX
	rx_metadata.waitForTimestamp = false; 	//currently has no effect in RX

	lms_stream_meta_t tx_metadata; 		//Use metadata for additional control over sample send function behavior
	tx_metadata.flushPartialPacket = false; //do not force sending of incomplete packet
	tx_metadata.waitForTimestamp = true; 	//Enable synchronization to HW timestamp

	lms_stream_status_t status;		// To check the FIFO


	// counters to keep track of the transmission FIFO
	int TXFIFO_slots = N_buffers_per_fifo;
	int ii_TXavg = 0;
	int ii_TXpcyc = 0;
	int ii_TXoffset = 0;
	int ii_TXrep = 0;
	int ii_sent = 0;
	double init_delay_s = 10e-3; // delay in seconds until TX packets are forwarded from FPGA to the FPRF
	long next_TXtimestamp = ceil(   (init_delay_s * LimeCfg.srate)  /  (double) buffersize) * buffersize;
	long last_TXtimestamp = 0; // this one stores the last timestamp of the beginning of a repetition

	// Timestamps to schedule the acquisition
	long next_RXtimestamp = 0;
	long last_RXtimestamp = 0;

	// Acquisition loop
	auto t1 = chrono::high_resolution_clock::now();
	auto t2 = t1;

	int samplesRead;
	int samplesReadSum = 0;
	int rcvattempts = 0;

	int ii_rep = 0;			// number of repetions
	int ii_pcyc = 0;		// number of phase cycle
	int ii_avg = 0;			// number of averages
	int ii_acqd = 0;		// number of complete acquisitions
	int ii_acq = -1;		// acquisition index (== ii_acqd if there is no packet loss)
	int samples2Acquire = 0;	// number of samples to acquire in current acquisition
	int validSamples = 0;	    	// number of valid samples in current datapacket
	int * acqbuf_pos;		// pointer to acqbuffer
	int * delayedacqbuf_pos;	// pointer to acqbuffer for delayed fwd
	int reps_btw_stamps;		// number of repetions between last valid timestamp
	int16_t * mirbuf_pos;		// pointer to mirror buffer


	bool acquiring = false;		// RX stream to acqbuffer?
	bool acquire = true;		// disable one single acquisition in acq loop
	bool delayedAcqbufFwd = false;	// to delay the forwarding of the acqbuffer

	int ndebug = 100;

	//Start streaming
	for (int i = 0; i < chCount; ++i)
	{
		LMS_StartStream(&rx_streams[i]);
		LMS_StartStream(&tx_streams[i]);
	}

	// pre-fill the TX fifo
	for (int ii_TXbuff = 0; ii_TXbuff < N_buffers_per_fifo; ii_TXbuff++) {

		// save the TX timestamp to the current packet
		tx_metadata.timestamp = next_TXtimestamp;

		// First packet is special, since it is cut off in some weird way
		if (ii_TXbuff == 0) {
			LMS_SendStream(&tx_streams[0], tx_buffer_1st, buffersize, &tx_metadata, 1000); // so we put zeros
			TXFIFO_slots--;

			// advance TX timestamp for the next packet
			next_TXtimestamp += rep_offset;

			next_RXtimestamp = next_TXtimestamp; // ... and do not wait for it
			last_TXtimestamp = next_TXtimestamp;
			continue; // proceed the for loop with the first actual TX packet
		} 

		// Put data to FIFO
		LMS_SendStream(&tx_streams[0], tx_buffer[ii_TXpcyc][ii_TXoffset], buffersize, &tx_metadata, 1000);

		// Update TX FIFO counters
		TXFIFO_slots--;
		ii_sent++;


		// advance the tx_buffer counter
		ii_TXoffset++;
		next_TXtimestamp += buffersize;
		if (ii_TXoffset == exc_buffers) {
			ii_TXoffset = 0;
			next_TXtimestamp = last_TXtimestamp + rep_offset;
			last_TXtimestamp = next_TXtimestamp;

			if (LimeCfg.pcyc_bef_avg > 0) {
				ii_TXpcyc++;
				if (ii_TXpcyc == num_phavar) {
					ii_TXpcyc = 0;
					ii_TXavg++;
					if (ii_TXavg == LimeCfg.averages) {
						ii_TXavg = 0;
						ii_TXrep++;
						// in case the entire experiment fits within the TX FIFO
						if (ii_TXrep == LimeCfg.repetitions){
						 TXFIFO_slots = 0;
						 break;
						}
					}
				}
			} else {
				ii_TXavg++;
				if (ii_TXavg == LimeCfg.averages) {
					ii_TXavg = 0;
					ii_TXpcyc++;
					if (ii_TXpcyc == num_phavar) {
						ii_TXpcyc = 0;
						ii_TXrep++;
						// in case the entire experiment fits within the TX FIFO
						if (ii_TXrep == LimeCfg.repetitions){
						 TXFIFO_slots = 0;
						 break;
						}
					}
				}
			}
		} else {
			// if there is still data to be put on the buffer
		}
	}

	/*
	// Check for the TX buffer and keep it filled
	LMS_GetStreamStatus(tx_streams, &status); //Obtain TX stream stats
	if (status.fifoFilledCount != 0) cout << TXFIFO_slots <<" TXFIFO slots free before start: " << status.fifoFilledCount << " samples of " << status.fifoSize << " with HW stamp " << status.timestamp <<" at RX timestamp" << rx_metadata.timestamp << endl;
	*/
	// Main acquisition loop
	while (ii_acq < LimeCfg.repetitions * LimeCfg.averages * num_phavar) 
	{

		//Receive samples
		if (acquire) {
			samplesRead = LMS_RecvStream(&rx_streams[0], buffers[0], buffersize, &rx_metadata, 1000);
			rcvattempts++;
			samplesReadSum += samplesRead;
		}

		if (ndebug < 100) {
			cout << rx_metadata.timestamp << ", " << samplesReadSum  << endl;
			ndebug++;
			LMS_GetStreamStatus(rx_streams, &status); //Obtain RX stream stats
			cout << "Rx stream info: " << status.overrun << ", " << status.underrun << status.droppedPackets << ", " << status.overrun << ", actually " << status.fifoFilledCount << endl;

		}

		// check if the scheduled timestamp is coming here
		//if (rx_metadata.timestamp >= next_RXtimestamp) {
		if ((rx_metadata.timestamp >= next_RXtimestamp - samplesRead + 1) && acquire) {

			// first check out scheduling
			timestampOffset = (signed long) next_RXtimestamp - (signed long) rx_metadata.timestamp;

			// normal case: scheduling as it should, where one reptime passed between the current and the last stamp
			reps_btw_stamps = 1; 

			// abnoral case: packet loss, i.e. more than one reptime passed since last stamp
			if (timestampOffset < 0) {
				reps_btw_stamps = ceil( -(double) timestampOffset / (double) rep_offset) +  1;
				//cout << "Acq: rep " << ii_rep << ", avg " << ii_avg << ", pcyc " << ii_pcyc << " : sched/act tstamp: " << next_RXtimestamp << ", " << rx_metadata.timestamp << "   Diff to last: " << next_RXtimestamp - last_RXtimestamp << " Offset: " <<  timestampOffset  << ", which corresponds to " << -(double) timestampOffset /(double) rep_offset << " repetitions, currently processing " << samplesRead << " RX samples with delayed fwd " << delayedAcqbufFwd << endl;

				// shift the timestamp scheduling correspondingly
				timestampOffset += (reps_btw_stamps-1) * rep_offset;
				next_RXtimestamp += (reps_btw_stamps-1) * rep_offset;

				// abort any ongoing acquisition, including delayed acquisition due to offsets
				if (acquiring) {
					cout << "Packet loss during rep " << ii_rep << ", avg " << ii_avg << ", pcyc " << ii_pcyc << ", acq " << ii_acq <<  ", acqd " << ii_acqd << ": " << samples2Acquire << " Samples were not written and only the first few samples are non-corrupted with certainty. " << endl;

					// substract the content of the mirror_buf from the acqbuf, just to avoid that crap is being kept on the main buffer.
					acqbuf_pos = acqbuf[ii_rep*num_phavar + ii_pcyc];
					for (int ii_acqbuf = 0; ii_acqbuf < 2*(rec_len - samples2Acquire); ii_acqbuf++) acqbuf_pos[ii_acqbuf] -= (int) mirror_buf[ii_acqbuf];

					// store that this is lost
					lost[ii_rep*num_phavar + ii_pcyc]++;
					lost_acqs.push_back(ii_acq);

					//ii_acq++; // for an ongoing acquisition, we still need to increment the acquisition counter
					// this is actually weird here. It seems that we land here sometimes with ii_acq already advanced
					// and sometimes with ii_acq still needing to be incremented.
					// in fact, when resuming, we are sometimes having ii_acq one before ii_avg, or aligned, as it should
					// so we do lose one acq and are moreover shifting the entire indexing. However, if ii_acq is uncommented, 
					// there is a segfault from advancing ii_acq once too few, so that it is better to keep this one
					// it is probably related to delayed acqbuf fwd. 
					// the cleanest would eventually be to make a new ii_acq counter that counts the memory location and is incremented together with the ii_pcyc counters, etc. The actual ii_acq that is incremented after having acquired data, could be named ii_acqd to count for the acquired data packets.

				}
				acquiring = false; // this will be reset to true just below, which will cause those unwritten samples
				delayedAcqbufFwd = false; // ... and make sure that these unwritten samples do not go anywhere to the buffer

			}

			// Advance counters to new position
			for (int ii = 0; ii < reps_btw_stamps; ii++) {
				
				// except at the very first acquisition, where the counters are already at the right position
				//if (ii_acq == 0 & ii == 0) break;

				// book keep any of the lost acquisitions
				if (ii > 0) {
					lost[ii_rep*num_phavar + ii_pcyc]++;
					lost_acqs.push_back(ii_acq);
				}

				ii_acq++;

				// except at the very first acquisition, where the counters are already at the right position
				if (ii_acq == 0) break;

				// advance counters
				if (LimeCfg.pcyc_bef_avg > 0) {
					ii_pcyc++;
					if (ii_pcyc == num_phavar) {
						ii_pcyc = 0;
						ii_avg++;
						if (ii_avg == LimeCfg.averages) {
							ii_avg = 0;
							ii_rep++;
						}
					}
				} else {
					ii_avg++;
					if (ii_avg == LimeCfg.averages) {
						ii_avg = 0;
						ii_pcyc++;
						if (ii_pcyc == num_phavar) {
							ii_pcyc = 0;
							ii_rep++;
						}
					}
				}

			}


			// additional reporting in case of packet loss
			if (reps_btw_stamps > 1) {

				cout << "   Resuming acq at rep " << ii_rep << ", avg " << ii_avg << ", pcyc " << ii_pcyc <<  ", acq " << ii_acq << ": " << "Skipped " << reps_btw_stamps - 1 << " acquisitions to restore a timestamp offset of " << timestampOffset << endl; 
			}	


			// Advance acqbuf in case that there is not an ongoing acquisition (just in the case of gap-free acquisition, that has usually a timestamp offset)
			if (acquiring == false) {
				acqbuf_pos = acqbuf[ii_rep*num_phavar + ii_pcyc];
				samples2Acquire = rec_len;
			} else { 
				delayedacqbuf_pos = acqbuf[ii_rep*num_phavar + ii_pcyc];
				delayedAcqbufFwd = true;
			}
			acquiring = true;

			//cout << "Now at rep " << ii_rep << ", avg " << ii_avg << ", pcyc " << ii_pcyc << ", acq " << ii_acq  << ", acqd " << ii_acqd << "."<< endl;


			// Warn in case of packet loss
			// Important: We exclude here packet loss at the very beginning of the RX stream. This is actually rather normal and the reason for the offset in the RX buffer
			LMS_GetStreamStatus(rx_streams, &status); //Obtain RX stream stats
			if ((status.droppedPackets > 0 | status.overrun > 0 | status.underrun > 0) & ii_acq > 0) {
				cout << "Rx stream trouble! Status (overrun, underrun, dropped Packets): " << status.overrun << ", " << status.underrun << ", " << status.droppedPackets << ". Currently " << status.fifoFilledCount << " samples in RX stream buffer (" << 100.0 * ((float) status.fifoFilledCount)/( (float) status.fifoSize ) << "%)" << endl;
				//cout << "Next acq: rep " << ii_rep << ", avg " << ii_avg << ", pcyc " << ii_pcyc << " : sched/act tstamp: " << next_RXtimestamp << ", " << rx_metadata.timestamp << "   Diff to last: " << next_RXtimestamp - last_RXtimestamp << " Offset: " <<  timestampOffset  << " currently processing " << samplesRead << " RX samples with delayed fwd " << delayedAcqbufFwd << endl;
			}


			// advance to the forthcoming RX timestamp and keep the current one
			next_RXtimestamp += rep_offset;
			last_RXtimestamp = rx_metadata.timestamp;
		}
		acquire = true;

		// Do not enter into acquiring for the case that the experiment is at its end
		if (ii_rep == LimeCfg.repetitions & delayedAcqbufFwd == false) break;

		// copy RX data into acquisition buffer
		if (acquiring) {

			// standard case: copy everything, without offset
			bufferOffset = 0;
			validSamples = buffersize;

			// first packet: consider eventual timestamp offset
			if (samples2Acquire == rec_len) {
				bufferOffset = timestampOffset;
				validSamples = buffersize - bufferOffset;

				mirbuf_pos = mirror_buf;
				// last packet with timestamp offset: just get the tail without offset
			} else if (samples2Acquire < buffersize) {
				validSamples = samples2Acquire;
			}

			for (int ii_acqbuf = 0; ii_acqbuf < 2*(validSamples); ii_acqbuf++) acqbuf_pos[ii_acqbuf] += (int) buffers[0][ii_acqbuf + 2* bufferOffset];
			samples2Acquire -= validSamples;

			// memcopy mirrorbuf
			memcpy(mirbuf_pos, acqbuf_pos, 2*validSamples * sizeof(int16_t));

			// advance position in acquisition buffer
			acqbuf_pos += 2*validSamples;
			mirbuf_pos += 2*validSamples;

			if (samples2Acquire == 0) {
				ii_acqd++; 


				// check for continuous RX with timestamp offset, where we would actually still have valid samples to copy in the buffer
				if (delayedAcqbufFwd) {
					// put pointer to right place 
					acqbuf_pos = delayedacqbuf_pos;
					samples2Acquire = rec_len;

					delayedAcqbufFwd = false;
					// important: rerun this entire block without getting a new data or forwarding the timestamp packet. 
					// We still need to copy the part beyond the validsamples to the next acqbuf position
					acquire = false;
				} else {
					// standard case: signal that the acquisition is finished and wait for the next scheduled timestamp
					acquiring = false;
				}
			}
		}

		// Check for the TX buffer and keep it filled
		if (ii_TXrep < LimeCfg.repetitions) {
			LMS_GetStreamStatus(tx_streams, &status); //Obtain TX stream stats
			TXFIFO_slots = (status.fifoSize - status.fifoFilledCount)/buffersize;
		}

		/*
		// debug
		if (TXFIFO_slots > 0) cout << TXFIFO_slots << " free fifo slots to fill" << endl;
		*/

		// re-fill the TX fifo
		while (TXFIFO_slots > 0) {

			// save the TX timestamp to the current packet
			tx_metadata.timestamp = next_TXtimestamp;

			// Put data to FIFO
			LMS_SendStream(&tx_streams[0], tx_buffer[ii_TXpcyc][ii_TXoffset], buffersize, &tx_metadata, 1000);

			// Update TX counters
			TXFIFO_slots--;
			ii_sent++;

			// advance the tx_buffer counter
			ii_TXoffset++;
			next_TXtimestamp += buffersize;
			if (ii_TXoffset == exc_buffers) {
				ii_TXoffset = 0;
				next_TXtimestamp = last_TXtimestamp + rep_offset;
				last_TXtimestamp = next_TXtimestamp;

				if (LimeCfg.pcyc_bef_avg > 0) {
					ii_TXpcyc++;
					if (ii_TXpcyc == num_phavar) {
						ii_TXpcyc = 0;
						ii_TXavg++;
						if (ii_TXavg == LimeCfg.averages) {
							ii_TXavg = 0;
							ii_TXrep++;
							// in case the experiment is finished
							if (ii_TXrep == LimeCfg.repetitions)
								TXFIFO_slots = 0;
						}
					}
				} else {
					ii_TXavg++;
					if (ii_TXavg == LimeCfg.averages) {
						ii_TXavg = 0;
						ii_TXpcyc++;
						if (ii_TXpcyc == num_phavar) {
							ii_TXpcyc = 0;
							ii_TXrep++;
							// in case the experiment is finished
							if (ii_TXrep == LimeCfg.repetitions)
								TXFIFO_slots = 0;
						}
					}
				}
			}
		}
}

//Stop streaming
for (int i = 0; i < chCount; ++i)
{
	LMS_StopStream(&rx_streams[i]); //stream is stopped but can be started again with LMS_StartStream()
	LMS_StopStream(&tx_streams[i]);
}
for (int i = 0; i < chCount; ++i)
{
	LMS_DestroyStream(device, &rx_streams[i]); //stream is deallocated and can no longer be used
	LMS_DestroyStream(device, &tx_streams[i]);
	delete[] buffers[i];
}

delete mirror_buf;

cout << "Lost acquisitions: ";
for (int ii = 0; ii < acqbuf_size; ii++) {
	cout << lost[ii] << ", ";
}
cout << endl;

// Iterate and print values of the list
for (int n : lost_acqs) {
	std::cout << n << '\n';
}

//------------------------------------------------------------------------------------- 
//					SAVE TO HDF5
//------------------------------------------------------------------------------------- 

if (LimeCfg.override_save == 0) {

	// Open HDF5 file
	string filename;
	// check for save_path delimiter
	if (LimeCfg.save_path.back() == '/')
		filename = LimeCfg.save_path + LimeCfg.file_stamp + "_" + LimeCfg.file_pattern + ".h5";
	else
		filename = LimeCfg.save_path + '/' + LimeCfg.file_stamp + "_" + LimeCfg.file_pattern + ".h5";
	cout << filename << endl;
	H5::H5File* h5f;

	// create or open
	if (file_exists(filename)) 	h5f = new H5::H5File( filename, H5F_ACC_RDWR );	
	else 				h5f = new H5::H5File( filename, H5F_ACC_EXCL );	

	// Check for the number of datasets already in there (only >0 if an external file_stamp is provided or if the program is called more than once within a second..)
	hsize_t  num_obj = 0;
	H5Gget_num_objs(h5f->getId(), &num_obj); // if success, num_obj will be assigned the number of objects in the group

	// write dataset to HDF5 file
	// 1. specify datatype and dimensions and dataset name
	H5::DataType	saveDataType( H5::PredType::NATIVE_INT);
	hsize_t saveDataDim[] = { (hsize_t) acqbuf_size, (hsize_t) 2*rec_len};
	string DataName = "Acqbuf_";
	std::ostringstream oss;
	oss << setfill('0') << setw(2) << num_obj;
	DataName += oss.str();

	H5std_string saveDataName(DataName.c_str());

	// 2. allocate dataspace and init
	// set parameters to have a chunked file, so that each acquired trace is one chunk
	H5::DSetCreatPropList cparms;
	hsize_t chunk_dims[2] = {1, saveDataDim[1]};
	cparms.setChunk(2, chunk_dims);

	int fill_val = 0;
	cparms.setFillValue (H5::PredType::NATIVE_INT , &fill_val);

	H5::DataSpace mspace1( 2, saveDataDim );
	H5::DataSet dataset = h5f->createDataSet(saveDataName, saveDataType, mspace1, cparms);

	// write with standard procedure
	//dataset.write( acqbuf, saveDataType); // requires contiguous memory of the entire acqbuf, which does not work for large buffers
	// write row-wise
	H5::DataSpace fspace_row = dataset.getSpace();
	hsize_t offset[2] = {0, 0};
	hsize_t dims_row[2] = {1, saveDataDim[1]};
	H5::DataSpace mspace_row( 1, &saveDataDim[1] ); // contiguous memory space of data to write
	for (int ii = 0; ii < acqbuf_size; ii++) {
		fspace_row.selectHyperslab( H5S_SELECT_SET, dims_row, offset);
		dataset.write( acqbuf[ii], saveDataType, mspace_row, fspace_row);
		offset[0] += 1; // advance to next row
	}

	// get the timestamp at the end of the experiment ...
	now = std::chrono::system_clock::now();
	itt = std::chrono::system_clock::to_time_t(now);
	stringstream.str("");
	stringstream.clear();
	stringstream << std::put_time(localtime(&itt), "%G%m%d_%H%M%S");

	// ... and write it to the appropriate index
	for (int ii_attr = 0; ii_attr < no_of_attr; ii_attr++) {
		if (strcmp("Exp End Timestamp", HDFattr[ii_attr].Name.c_str()) == 0) {
			LimeCfg.stamp_end	= stringstream.str();
			HDFattr[ii_attr].dType = H5::StrType(H5::PredType::C_S1, LimeCfg.stamp_end.length()+1);
			HDFattr[ii_attr].Value = (void *) LimeCfg.stamp_end.c_str();
		}
	}

	// write the attributes	
	for (int ii = 0; ii < no_of_attr; ii++) {

		H5::DataSpace* tmpSpace = new H5::DataSpace();
		// special case: arrays
		if (HDFattr[ii].dim > 1) {
			delete tmpSpace;
			H5::DataSpace* tmpSpace = new H5::DataSpace(1, &HDFattr[ii].dim);
		}
		H5std_string concat("-" + HDFattr[ii].arg + " "  + HDFattr[ii].Name);
		//H5::Attribute attribute = h5f->createAttribute(concat, HDFattr[ii].dType, *tmpSpace); // write the attribute to the file
		H5::Attribute attribute = dataset.createAttribute(concat, HDFattr[ii].dType, *tmpSpace); // write the attribute to the dataset
		attribute.write(HDFattr[ii].dType, HDFattr[ii].Value);
		delete tmpSpace;
	}

	// special attribute for N pulses: the phase table, which is certainly of use in evaluation
	hsize_t phatab_len = LimeCfg.Npulses*num_phavar;
	H5::DataSpace* tmpSpace = new H5::DataSpace(1, &phatab_len);
	H5std_string concat("-/// Phase Table");
	H5::Attribute attribute = dataset.createAttribute(concat, H5::PredType::IEEE_F64LE, *tmpSpace); // write the attribute to the dataset
	attribute.write( H5::PredType::IEEE_F64LE, &pha_tab);
	delete tmpSpace;

	// close file
	h5f->close();
	delete h5f;

	cout << "Written to HDFfile as " << saveDataDim[0] << " by "<< saveDataDim[1] << " array" << endl;

}

//Close device
LMS_Close(device);

return 0;
}



