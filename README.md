
# Whisper2Clip: Audio Recording with Transcription
This Python script allows users to record audio using their microphone and transcribe the recorded audio using 
the Whisper transcription model. It provides a simple hotkey to start and stop recording using a customizable 
hotkey combination.


## Features
- Start and stop recording using a hotkey combination
- Transcribe recorded audio using the `Whisper` model from OpenAI (free and offline)
- Copy the transcription to the clipboard automatically


## Prerequisites
- Python 3.7, 3.8, 3.9
- CUDA is highly recommended for performance


## Installation
1. Install `PyTorch` for python. Refer to the [PyTorch's website](https://pytorch.org/get-started/locally/) for details
2. Clone this repository and install the requirements
   ```
   git clone https://github.com/Crossoufire/whisper2clip.git
   cd whisper2clip
   pip install -r requirements.txt
   ```
3. Install `Ffmpeg` and add it to the PATH (necessary for the Whisper model)


### First Start - Choosing A Whisper Model
- When executing this script for the first time will download the chosen Whisper model (`default: medium.en` about `1.4Gb`)
- Based on your GPU VRAM, choose the appropriate Whisper model for optimal performance
- Below is a table of available models with their required VRAM and relative speed

|  Size  | Required VRAM | Relative speed |
|:------:|:-------------:|:--------------:|
|  tiny  |     ~1 GB     |      ~32x      |
|  base  |     ~1 GB     |      ~16x      |
| small  |     ~2 GB     |      ~6x       |
| medium |     ~5 GB     |      ~2x       |
| large  |    ~10 GB     |       1x       |

- For English-only applications, the `.en` models (e.g., `tiny.en`, `base.en`) tend to perform better
- To change the model, modify these lines in the `main()` function of the `main.py` script
```
hotkey = "ctrl+alt+space"
model_name = WhisperModels.MEDIUM_EN
```
- The available `WhisperModels` are the same as presented in the table above as Python Enum.


## Usage
- Run the application
```
python main.py
```
- Enter the hotkey to start recording (default: `ctrl+alt+space`) and again to stop recording
- Transcription will be automatically copied to your clipboard


## Acknowledgments
- This project uses the OpenAI's [Whisper](https://github.com/openai/whisper) model for the audio transcription
- This project is forked and modified from the original creator [gustavostz](https://github.com/gustavostz/whisper-clip)
