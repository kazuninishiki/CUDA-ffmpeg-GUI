# CUDA-ffmpeg-GUI

h265 / x264 accelerated ffmpeg encoder GUI with frame interpolation options.

Uses precompiled CUDA-enabled ffmpeg from here: https://www.gyan.dev/ffmpeg/builds/

You'll need ffmpeg.exe and ffprobe.exe from gyan.dev's packages in the same folder where this python script is executed (or in environment variable).

![image](https://github.com/kazuninishiki/CUDA-ffmpeg-GUI/assets/21254414/09b794fa-f002-4109-98c8-cb10ea0a3f82)


Let me know if you have any questions.

**Options:**

minterpolate : _interpolates frames to 60fps, similar to SVP's SVPEncode._
<br>
**-vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"**
<br><br><br>


hwaccel_output_format cuda : _Full hardware transcode with NVENC Encoding_
<br>
**-hwaccel_output_format cuda** 
<br><br><br>




hwaccel cuda : _Full hardware transcode with NVDEC decoding_
<br>
**-hwaccel cuda**
<br><br><br>



hevc_nvenc/h264  : _uses CUDA for accelerated h264 or h265(hevc) encoding.  Must be combined with "CUDA output" Checked._
<br>
**-c:v hevc_nvenc or h264_nvenc** 
<br><br><br>

save/load  : _save or load the existing command shown in textbox for future reference to reuse the parameters._
<br>
<br><br><br>
