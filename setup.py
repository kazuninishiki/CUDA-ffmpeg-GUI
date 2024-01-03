from cx_Freeze import setup, Executable

setup(
    name="VideoConverterApp",
    version="1.0",
    description="Video Converter Application",
    executables=[Executable("video_converter_app.py", base="Win32GUI")],
)
