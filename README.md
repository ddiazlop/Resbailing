# Resbailing

An implementantion using models from HuggingFace to generate powerpoint presentations given a markdown document or an audio file. Initially developed as my end of degree project.
The application interface is currently using the Kivy Framework, since most computations are made on the end user's machine.

## Features
- Automatically divides the text into semantically similar sections that represent each of the slides.
- Resumes the content to fit the size of the slide.
- Generates an image for the slide.
- Support for various Markdown formats (Title & Text, Title & Sections & Text, No format) and .mp3 or .wav audio files.
- Various expandable output styles.
- Export to Google Slides with the Google Slides API.
