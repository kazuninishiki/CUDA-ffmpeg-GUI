The "peeudocode" I've used for GPT prompt is as follows.
As mentioned, they were not perfect but can do mostly what
I have wanted / instructed it to do.

There are minor revisions to the code (such as crf being 16 not 19), which was manually adjusted in the actual python source.

________________________________________________________
write a python script that opens a window that accepts 2 text input, first one labeled "source" and second as "destination".  both are file pickers, and it allows user to type in the path in the window also.
destination path will be filled in with the same path used from "source" entered by user, but remove the extension.

once user clicks submit on the window, it will run a windows command with the below syntax:

ffmpeg -y -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1 -hwaccel cuda -hwaccel_output_format cuda -i <source> -c:a copy  -c:v h264_nvenc <destination>

capture the output from this command into a continuously scrolling text window in the same parent window as the input dialog box.

modify the windowed output for the generated messaages from ffmpeg command to keep all history and with a verticle scrollbar so user can view preivous messages.  also make the message having at least 132 character width.  use consolas font. resizing the window also appropriately resizes the output text box.

at the end of the command when it is completed. display a button that says it is done. once user is clicked, the user can now continue to submit other files for processing.

when the processing is down, use ffmpeg or ffprobe to check the source and destination file's video length and display them beside the browse button.

use a checkbox to enable the ffmpeg option '-vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"' .  the label of the checkbox is "minterpolate".

use a checkbox to enable the ffmpeg option "-hwaccel cuda"

use a checkbox to enable the ffmpeg option "-hwaccel_output_format cuda"

use two radio buttons to enable the ffmpeg option "-c:v h264_nvenc" or "-c:v h265_nvenc".  the second option is ticked by default.

add a textbox to show the executed command for ffmpeg before executing.  the command textbox should be above the ffmpeg output textbox.

add a STOP button so that it can kill the ffmpeg process in order to abort the execution.

add a slider to adjust the value for ffmpeg's command parameter "-crf 19" where the value in the slider can be from 16 to 24".  default to 16.

