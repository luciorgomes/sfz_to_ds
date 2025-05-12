# Sfz to Decentsampler

Convert sfz files to decentsampler format.

![Captura de imagem_20250511_213715](https://github.com/user-attachments/assets/f471ccc1-eeba-4169-ae7a-94d1bbf1ebf7)

The first option creates an individual .dspreset file converted from the .sfz file with the name of the "Name output" text control.

The second will scan all .sfz files in the folder "Folder to Scan" (and subfolders) and create a .dspreset with the same name.

The files are created in the same folder of the .sfz file.

Selecting the "Effects" checkbox the .dspreset will bring knobs to control most of the internal effects of DecentSampler

![Captura de imagem_20250511_214542](https://github.com/user-attachments/assets/560986d0-ec28-4939-9452-ca3344e86645)

If you create a symlink in the DecentSampler folder to the Sfz folder you can use the file browser to select the generated files.

![Captura de imagem_20250511_214625](https://github.com/user-attachments/assets/294a32dd-7388-44e7-9e3d-7b2cf454b335)

It's a simple script, it may will not work in more complex .Sfz files

Requirements:
Python 3
WxPython


