# -*- coding: utf-8 -*-
"""SPEC_AUG30%.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SpbMciP1rZ9B3YtPfm5jpZiYi7Fx0flE
"""

#authentication
from google.colab import auth
auth.authenticate_user()

#accessing cloud data
!echo "deb http://packages.cloud.google.com/apt gcsfuse-bionic main" > /etc/apt/sources.list.d/gcsfuse.list
!curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
!apt -qq update
!apt -qq install gcsfuse

!mkdir colab_direcoty
!gcsfuse --implicit-dirs aug-1 colab_direcoty

!wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb
!dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb
!apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
!apt-get update
!apt-get install cuda=9.0.176-1

#required libraries
#!pip3 install sox
!pip install audiomentations==0.20.0
!pip install tensorflow==1.14.0
!pip install tensorflow-gpu==1.14.0
!pip install q keras==2.3.1
!pip install h5py==2.10.0
#!pip install torch-audiomentations
#!pip install nlpaug
#!pip install audiomentations
!pip install librosa --upgrade
#!pip install librosa==0.8.1
#!pip install pydub==0.25.1
#!pip install -r/content/colab_direcoty/requirements.txt

!python batch_feature_extraction.py

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master

#!pip install nlpaug
#!pip install librosa
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift
import librosa.display

import scipy.io.wavfile as wav
#import nlpaug.augmenter#masking
#from nlpaug.augmenter import spectrogram as nas#masking
#from audiomentations import SpecCompose, SpecChannelShuffle, SpecFrequencyMask#masking
import numpy as np
import librosa
#import nlpaug.augmenter#masking
#from nlpaug.augmenter import spectrogram as nas#masking
import matplotlib.pyplot as plot
import matplotlib.gridspec as gridspec
#aug = nas.TimeMaskingAug(zone=(0.2, 0.3), coverage=1)#time masking
#augment = SpecCompose([SpecFrequencyMask([(( ([max_mask_fraction: float = 0.25]), p=0.3)])
#mask_fraction = 0.05
#transform = SpecFrequencyMask(fill_mode="constant",fill_constant=0.0,min_mask_fraction=0.05,max_mask_fraction=0.07,p=0.4)
#augmented_spectrogram = transform(magnitude_spectrogram)

def _spectrogram(audio_input):
        #transform = SpecFrequencyMask(fill_mode="constant",fill_constant=0.0,min_mask_fraction=0.07,max_mask_fraction=0.09,p=0.4)
        _max_feat_frames=3000
        _win_len=960
        _nfft=1024
        _hop_len=480
        _nb_ch = audio_input.shape[1]
        nb_bins = _nfft // 2
        spectra = np.zeros((_max_feat_frames, nb_bins + 1, _nb_ch), dtype=complex)
        for ch_cnt in range(_nb_ch):
            stft_ch = librosa.core.stft(np.asfortranarray(audio_input[:, ch_cnt]), n_fft=_nfft, hop_length=_hop_len,
                                        win_length=_win_len, window='hann')
            #stft_ch=transform(stft_ch)#frequency masking
            print("hi")
            spectra[:, :, ch_cnt] = stft_ch[:, :_max_feat_frames].T
        return spectra

def _load_audio(audio_path):
        fs, audio = wav.read(audio_path)
        #print(audio)
        _nb_channels = 4
        _eps = 1e-8
        _audio_max_len_samples=1440000 #60*24000
        audio = audio[:,:_nb_channels] / 32768.0 + _eps
        if audio.shape[0] < _audio_max_len_samples:
            zero_pad = np.random.rand(_audio_max_len_samples - audio.shape[0], audio.shape[1])*_eps
            audio = np.vstack((audio, zero_pad))
        elif audio.shape[0] > _audio_max_len_samples:
            audio = audio[:_audio_max_len_samples, :]
        print("hi")
        augment = Compose([AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.4),])
        audio = augment(samples=audio, sample_rate=24000)
        return audio, fs

a1,f1=_load_audio("/content/sample_data/fold1_room1_mix001_ov1.wav")
print(a1.shape)

stft = np.abs(np.squeeze(_spectrogram(a1[:, :1])))
stft = librosa.amplitude_to_db(stft, ref=np.max)

plot.figure(figsize=(20, 15))
gs = gridspec.GridSpec(4, 4)


ax0 = plot.subplot(gs[0, 1:3]), librosa.display.specshow(stft.T,sr=f1, x_axis='s', y_axis='log'), plot.xlim([0, 60]), plot.xticks([]), plot.xlabel('time'), plot.title('Spectrogram')

#spec augment with guassian noise

stft = np.abs(np.squeeze(_spectrogram(a1[:, :1])))
stft = librosa.amplitude_to_db(stft, ref=np.max)

plot.figure(figsize=(20, 15))
gs = gridspec.GridSpec(4, 4)


ax0 = plot.subplot(gs[0, 1:3]), librosa.display.specshow(stft.T,sr=f1, x_axis='s', y_axis='log'), plot.xlim([0, 60]), plot.xticks([]), plot.xlabel('time'), plot.title('Spectrogram')

!python batch_feature_extraction.py #dev

!python batch_feature_extraction.py #eval

!python seld.py 4 #frequency masking

!python calculate_dev_results_from_dcase_output.py #freq aug

!python seld.py

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py

def _load_audio(audio_path):
        fs, audio = wav.read(audio_path)
        _nb_channels = 4
        _eps = 1e-8
        _audio_max_len_samples=1440000 #60*24000
        audio = audio[:,:_nb_channels] / 32768.0 + _eps
        if audio.shape[0] < _audio_max_len_samples:
            zero_pad = np.random.rand(_audio_max_len_samples - audio.shape[0], audio.shape[1])*_eps
            audio = np.vstack((audio, zero_pad))
        elif audio.shape[0] > _audio_max_len_samples:
            audio = audio[:_audio_max_len_samples, :]
        augment = Compose([AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.3),
                          #TimeStretch(min_rate=0.8, max_rate=1.25,p=0.3),
                          #PitchShift(min_semitones=-1, max_semitones=1,p=0.3),
                          #Shift(min_fraction=-0.5, max_fraction=0.5, p=0.3),
                          ])
        #audio=np.reshape(audio, (4, 1440000))
        #audio = augment(audio,24000)
        #audio=np.reshape(audio, (1440000,4))
        return audio, fs

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
#input_data = wav.read("/content/colab_direcoty/foa_dev/fold1_room1_mix001_ov1.wav")
#input_data1=wav.read("/content/fold1_room1_mix001_ov1.wav")
#fs, audio = wav.read(audio_path)

#audio = input_data[1]
audio=a2[1]
print(audio)
#audio2=audio2[:5000]
#audio1 = input_data[0]
#print(audio1)
#plt.figure(figsize=[15,14])
pyplot.xscale('log')
plt.plot(np.linspace(0, 1, len(audio[0:24000])), audio[0:24000])
#plt.plot(np.linspace(0, 1, len(audio2[0:24000])), audio2[0:24000])
plt.plot(audio[0:24000])
#plt.grid(c='grey')

#plt.plot(audio2[0:5000])
plt.grid(c='grey')

plt.ylabel("Amplitude")
plt.xlabel("Time")
plt.show()
#fig, axs = plt.subplots(2)
#fig.suptitle('Vertically stacked subplots')
#axs[0].plot(audio[0:24000])
#plt.grid(c='grey')

#axs[1].plot(audio2[0:24000])
#plt.grid(c='grey')
#plt.savefig('f1.png')

from audiomentations import LowPassFilter
import librosa.display
import IPython.display
import soundfile
import torchaudio
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plot



a2,f2=_load_audio("/content/colab_direcoty/foa_dev/fold1_room1_mix001_ov1.wav")
print(a2.shape)

def _spectrogram(audio_input):
        #transform = SpecFrequencyMask(fill_mode="constant",fill_constant=0.0,min_mask_fraction=0.05,max_mask_fraction=0.07,p=0.4)
        #/augment=LowPassFilter(min_cutoff_freq=512,max_cutoff_freq=1000,p=0.5)
        _max_feat_frames=3000
        _win_len=960
        _nfft=1024
        _hop_len=480
        _nb_ch = audio_input.shape[1]
        nb_bins = _nfft // 2
        spectra = np.zeros((_max_feat_frames, nb_bins + 1, _nb_ch), dtype=complex)
        for ch_cnt in range(_nb_ch):
            stft_ch = librosa.core.stft(np.asfortranarray(audio_input[:, ch_cnt]), n_fft=_nfft, hop_length=_hop_len,
                                        win_length=_win_len, window='hann')
            #stft_ch=transform(stft_ch)#frequency masking

            print("hi")
            spectra[:, :, ch_cnt] = stft_ch[:, :_max_feat_frames].T
        return spectra

stft = np.abs(np.squeeze(_spectrogram(a2[:, :1])))
stft = librosa.amplitude_to_db(stft, ref=np.max)

plot.figure(figsize=(20, 15))
gs = gridspec.GridSpec(4, 4)


ax0 = plot.subplot(gs[0, 1:3]), librosa.display.specshow(stft.T,sr=24000, x_axis='s', y_axis='log'), plot.xlim([0, 60]), plot.xticks([]), plot.xlabel('time'), plot.title('Spectrogram')

def plot_waveform(waveform, sample_rate, title="Waveform", xlim=None):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
        if xlim:
            axes[c].set_xlim(xlim)
    figure.suptitle(title)
    plt.show(block=False)

def plot_specgram(waveform, sample_rate, title="Spectrogram", xlim=None):
    waveform = waveform.numpy()

    num_channels, _ = waveform.shape

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
        if xlim:
            axes[c].set_xlim(xlim)
    figure.suptitle(title)
    plt.show(block=False)

plot_waveform(waveform1, sample_rate1, title="Original", xlim=(-0.1, 3.2))
plot_specgram(waveform1, sample_rate1, title="Original", xlim=(0, 3.04))
Audio(waveform1, rate=sample_rate1)

plot_waveform(waveform2, sample_rate2, title="Effects Applied", xlim=(-0.1, 3.2))
plot_specgram(waveform2, sample_rate2, title="Effects Applied", xlim=(0, 3.04))
Audio(waveform2, rate=sample_rate2)

pathAudio="/content/colab_direcoty/foa_dev"
files = librosa.util.find_files(pathAudio, ext=['wav'])
files = np.asarray(files)
i=0
for y1 in files:
    i=i+1
    print(i)
    k1=os.path.basename(y1)
    m1,n1= os.path.splitext(k1)
    print(m1)
    wave, sample = torchaudio.load(y1)

    if i%5==0:
    # Define effects
      effects = [
                 ["lowpass", "-2", "1000"],  # apply single-pole lowpass filter
                 #["speed", "0.8"],  # reduce the speed
                 #["rate", f"{sample_rate1}"],
                 #["reverb", "-w"],  # Reverbration gives some dramatic feeling
      ]
      wave1, sample1 = torchaudio.sox_effects.apply_effects_tensor(wave, sample, effects)
      print(wave1.shape)
      print("hi")
      path="/content/sample_data/foa_dev/"+f"{m1}.wav"
      torchaudio.save(path, wave1, sample_rate=24000)
    else:
      print(wave.shape)
      print("bye")
      path="/content/sample_data/foa_dev/"+f"{m1}.wav"
      torchaudio.save(path, wave, sample_rate=24000)

!zip -r /content/sample_data/foa_dev.zip /content/sample_data/foa_dev

!cp -r "/content/sample_data/foa_dev.zip" "/content/colab_direcoty/seld-dcase2020-master/c"

!python batch_feature_extraction.py  #low pass filter 1000hz

!python seld.py 4 #low-pass(50% of data with 1000 hz cutt-off frequency) and 6db attenuation after that

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py

!python seld.py

!python seld.py 5

# feature extraction for 40% guassian noise with 40% frequency mask

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master
!python batch_feature_extraction.py

!python batch_feature_extraction.py #(without aug for eval)

!python seld.py 4

!python seld.py

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master
!python calculate_dev_results_from_dcase_output.py

!python calculate_dev_results_from_dcase_output.py

# low pass with 2500 hz

def _load_audio(audio_path):
        effects = [
                 ["lowpass", "-2", "2500"],  # apply single-pole lowpass filter
                 #["speed", "0.8"],  # reduce the speed
                 #["rate", f"{sample_rate1}"],
                 #["reverb", "-w"],  # Reverbration gives some dramatic feeling
                  ]


        audio, fs = torchaudio.load(audio_path)
        #fs, audio = wav.read(audio_path)
        _nb_channels = 4
        _eps = 1e-8
        _audio_max_len_samples=1440000 #60*24000
        audio = audio[:_nb_channels,:] / 32768.0 + _eps
        if audio.shape[1] < _audio_max_len_samples:
            zero_pad = np.random.rand(_audio_max_len_samples - audio.shape[1], audio.shape[0])*_eps
            audio = np.vstack((audio, zero_pad))
        elif audio.shape[1] > _audio_max_len_samples:
            audio = audio[:_audio_max_len_samples, :]
        audio, _ = torchaudio.sox_effects.apply_effects_tensor(audio,24000, effects)
        print("hi")
        return audio, fs

def _spectrogram(audio_input):
        #transform = SpecFrequencyMask(fill_mode="constant",fill_constant=0.0,min_mask_fraction=0.05,max_mask_fraction=0.07,p=0.4)
        #augment=LowPassFilter(min_cutoff_freq=512,max_cutoff_freq=4096,p=0.5)
        _max_feat_frames=3000
        _win_len=960
        _nfft=1024
        _hop_len=480
        _nb_ch = audio_input.shape[0]
        nb_bins = _nfft // 2
        spectra = np.zeros((_max_feat_frames, nb_bins + 1, _nb_ch), dtype=complex)
        for ch_cnt in range(_nb_ch):
            stft_ch = librosa.core.stft(np.asfortranarray(audio_input[ch_cnt,:]), n_fft=_nfft, hop_length=_hop_len,
                                        win_length=_win_len, window='hann')
            #stft_ch=transform(stft_ch)#frequency masking
            print("hi")
            spectra[:, :, ch_cnt] = stft_ch[:, :_max_feat_frames].T
        return spectra

stft = np.abs(np.squeeze(_spectrogram(a2[:1,:])))
stft = librosa.amplitude_to_db(stft, ref=np.max)

plot.figure(figsize=(20, 15))
gs = gridspec.GridSpec(4, 4)


ax0 = plot.subplot(gs[0, 1:3]), librosa.display.specshow(stft.T,sr=24000, x_axis='s', y_axis='log'), plot.xlim([0, 60]), plot.xticks([]), plot.xlabel('time'), plot.title('Spectrogram')

a2,f2=_load_audio("/content/sample_data/fold1_room1_mix001_ov1.wav")
print(a2.shape)

import audiomentations
import torchaudio
import numpy as np
import librosa.display
import os
import soundfile as sf

pathAudio="/content/colab_direcoty/foa_dev"
files = librosa.util.find_files(pathAudio, ext=['wav'])
files = np.asarray(files)
i=0
for y1 in files:
    i=i+1
    print(i)
    k1=os.path.basename(y1)
    m1,n1= os.path.splitext(k1)
    print(m1)
    wave, sample = torchaudio.load(y1)

    if i%5==0:
    # Define effects
      effects = [
                 ["lowpass", "-2", "2500"],  # apply single-pole lowpass filter
                 #["speed", "0.8"],  # reduce the speed
                 #["rate", f"{sample_rate1}"],
                 #["reverb", "-w"],  # Reverbration gives some dramatic feeling
      ]
      wave1, sample1 = torchaudio.sox_effects.apply_effects_tensor(wave, sample, effects)
      print(wave1.shape)
      print("hi")
      path="/content/sample_data/foa_dev1/"+f"{m1}.wav"
      torchaudio.save(path, wave1, sample_rate=24000)
    else:
      print(wave.shape)
      print("bye")
      path="/content/sample_data/foa_dev1/"+f"{m1}.wav"
      torchaudio.save(path, wave, sample_rate=24000)

!zip -r /content/sample_data/foa_dev1.zip /content/sample_data/foa_dev1

!cp -r "/content/sample_data/foa_dev1.zip" "/content/colab_direcoty/seld-dcase2020-master/c"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master #low pass with 2500hz
!python batch_feature_extraction.py

!python seld.py 4

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py

# guassian noise 30% data set

"""**<h3> guassian noise 30% data set</h3>**

"""

!python batch_feature_extraction.py

!python seld.py 4

!python seld.py

!python calculate_dev_results_from_dcase_output.py

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py

!python visualize_SELD_output.py

#time stretch

"""#time stretch"""

def _load_audio(audio_path):
        augment = Compose([#AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.3),
                          #TimeStretch(min_rate=0.8, max_rate=1.25,p=0.3),
                          PitchShift(min_semitones=-1, max_semitones=1,p=1),
                          #Shift(min_fraction=-0.5, max_fraction=0.5, p=0.3),
                          ])

        fs, audio = wav.read(audio_path)
        _nb_channels = 4
        _eps = 1e-8
        _audio_max_len_samples=1440000 #60*24000
        audio = audio[:_nb_channels,:] / 32768.0 + _eps
        if audio.shape[1] < _audio_max_len_samples:
            zero_pad = np.random.rand(_audio_max_len_samples - audio.shape[1], audio.shape[0])*_eps
            audio = np.vstack((audio, zero_pad))
        elif audio.shape[1] > _audio_max_len_samples:
            audio = audio[:_audio_max_len_samples, :]
        audio=np.reshape(audio, (4, 1440000))
        print(audio.shape)
        audio = augment(audio,24000)
        audio=np.reshape(audio, (1440000,4))
        print("hi")
        return audio, fs

i1,i2=_load_audio("/content/sample_data/fold1_room1_mix001_ov1.wav")
print(i1.shape)

!python batch_feature_extraction.py

!python seld.py 4

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master
!python seld.py

!python calculate_dev_results_from_dcase_output.py

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py



"""pitch shift"""

!python batch_feature_extraction.py

!python seld.py 4

!python seld.py 5

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/colab_direcoty/seld-dcase2020-master

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py



"""**shift**"""

!python batch_feature_extraction.py

!python seld.py

!python seld.py 5

!python calculate_dev_results_from_dcase_output.py

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py



"""**frequency and time masking 30%**

"""

def _load_audio(audio_path):
        fs, audio = wav.read(audio_path)
        #print(audio)
        _nb_channels = 4
        _eps = 1e-8
        _audio_max_len_samples=1440000 #60*24000
        audio = audio[:,:_nb_channels] / 32768.0 + _eps
        if audio.shape[0] < _audio_max_len_samples:
            zero_pad = np.random.rand(_audio_max_len_samples - audio.shape[0], audio.shape[1])*_eps
            audio = np.vstack((audio, zero_pad))
        elif audio.shape[0] > _audio_max_len_samples:
            audio = audio[:_audio_max_len_samples, :]
        print("hi")
        #augment = Compose([AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.4),])
        #audio = augment(samples=audio, sample_rate=24000)
        return audio, fs

from audiomentations.augmentations.transforms import TimeMask
from audiomentations import SpecFrequencyMask
def _spectrogram(audio_input):
        transform = SpecFrequencyMask(fill_mode="constant",fill_constant=0.0,min_mask_fraction=0.06,max_mask_fraction=0.06,p=0.3)
        aug=TimeMask(max_band_part=0.03,min_band_part=0.03,p=0.3)
        _max_feat_frames=3000
        _win_len=960
        _nfft=1024
        _hop_len=480
        _nb_ch = audio_input.shape[1]
        nb_bins = _nfft // 2
        spectra = np.zeros((_max_feat_frames, nb_bins + 1, _nb_ch), dtype=complex)
        for ch_cnt in range(_nb_ch):
            stft_ch = librosa.core.stft(np.asfortranarray(audio_input[:, ch_cnt]), n_fft=_nfft, hop_length=_hop_len,
                                        win_length=_win_len, window='hann')
            stft_ch=transform(stft_ch)#frequency masking
            stft_ch=aug(stft_ch,24000)
            print("hi")
            spectra[:, :, ch_cnt] = stft_ch[:, :_max_feat_frames].T
        return spectra

stft = np.abs(np.squeeze(_spectrogram(a2[:, :1])))
stft = librosa.amplitude_to_db(stft, ref=np.max)

plot.figure(figsize=(20, 15))
gs = gridspec.GridSpec(4, 4)


ax0 = plot.subplot(gs[0, 1:3]), librosa.display.specshow(stft.T,sr=24000, x_axis='s', y_axis='log'), plot.xlim([0, 60]), plot.xticks([]), plot.xlabel('time'), plot.title('Spectrogram')

a2,f2=_load_audio("/content/sample_data/fold1_room1_mix001_ov1.wav")
print(a2.shape)

!python batch_feature_extraction.py

!python batch_feature_extraction.py

!python seld.py 4

!python batch_feature_extraction.py #20% time+freq

!python batch_feature_extraction.py

!python seld.py

#30% 0.06 freq and 0.03 time

!python batch_feature_extraction.py

!python seld.py 4



#t:20% and f:40%

!python batch_feature_extraction.py

!python seld.py 4

!python seld.py 5

!python calculate_dev_results_from_dcase_output.py

!python calculate_dev_results_from_dcase_output.py

!python visualize_SELD_output.py

