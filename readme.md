## Auto Source Video Render

A Python-based solution to automate the rendering of demos using [SourceDemoRender](https://github.com/crashfort/SourceDemoRender). Originally a private tool made by exer.

### Dependencies

[SourceDemoRender](https://github.com/crashfort/SourceDemoRender)

### Usage

- Change directories in both .py files to work with your setup
- Put 'AutoSVR' folder in prec folder
- Create a text file with RecordTitles somewhere in its name
- Copy demo titles from KillStreaks.txt from P-REC folder into RecordTitles.txt
- Add quotes around each title; make sure each title is on its own line
- Run AutoSVR.py
- Launch game with SourceDemoRender and start recording
- Play your first demo

The script will go through each demo and automatically record it for you.

### Settings for SVR's default.ini

This was given to me by exer, so when he sent this to me he also sent me his SVR settings. I'll partially preserve them here.

- motion_blur_enabled=1
- motion_blur_exposure=0.2
