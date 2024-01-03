# CUDA-ffmpeg-GUI

h265 / x264 accelerated ffmpeg encoder GUI with frame interpolation options.

Uses precompiled CUDA-enabled ffmpeg from here: https://www.gyan.dev/ffmpeg/builds/

You'll need ffmpeg.exe and ffprobe.exe from gyan.dev's packages in the same folder where this python script is executed (or in environment variable).

![image](https://github.com/kazuninishiki/CUDA-ffmpeg-GUI/assets/21254414/edacb1cc-ff3a-40f8-9ea9-393e461f412a)

Let me know if you have any questions.

**Options:**

motion interpolation : _interpolates frames to 60fps, similar to SVP's SVPEncode._

**-vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"**
:-:-



CUDA output : _Full hardware transcode with NVENC Encoding_

**-hwaccel_output_format cuda** 
:-
:-




CUVID Accel : _Full hardware transcode with NVDEC decoding_

**-hwaccel cuda**
:-:-



CUDA h264/h265  : _uses CUDA for accelerated h264 or h265 encoding.  Must be combined with "CUDA output" Checked._

**-c:v hevc_nvenc or h264_nvenc** 
:-:-
