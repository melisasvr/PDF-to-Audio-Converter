# PDF to Audio Converter
- A Python GUI application that converts PDF documents to audio files using text-to-speech technology. 
- Perfect for creating audiobooks, accessibility purposes, or listening to documents on the go.

## Features
- 📁 **Multiple PDF Support**: Select and convert multiple PDF files at once
- 🎯 **Dual Conversion Modes**: Create separate audio files or combine all PDFs into one
- 🎤 **Voice Customization**: Choose from available system voices and adjust speech rate
- 📊 **Progress Tracking**: Real-time progress bar and status updates
- 🖥️ **User-Friendly GUI**: Simple, intuitive interface built with tkinter
- ⚡ **Background Processing**: Non-blocking conversion with threading
- 🛡️ **Error Handling**: Robust error handling with detailed feedback

## Requirements
### Python Version
- Python 3.6 or higher

### Required Packages
```bash
pip install pyttsx3 PyPDF2
```

### System Requirements
- **Windows**: Built-in SAPI voices
- **macOS**: Built-in system voices
- **Linux**: espeak or festival (install via package manager)

## Installation

1. **Clone or download** this repository to your local machine

2. **Install dependencies**:
   ```bash
   pip install pyttsx3 PyPDF2
   ```

3. **Run the application**:
   ```bash
   python pdf_to_audio_converter.py
   ```

## Usage

### Basic Usage

1. **Launch the application**
   ```bash
   python pdf_to_audio_converter.py
   ```

2. **Add PDF files**
   - Click the "Add PDF Files" button
   - Select one or multiple PDF files from your computer
   - Selected files will appear in the list

3. **Configure settings**
   - Adjust speech rate (100-300 WPM)
   - Select preferred voice from the dropdown
   - Choose output name/prefix

4. **Select conversion mode**
   - **Separate Files**: Creates individual audio files for each PDF
   - **Combined**: Merges all PDFs into one audio file

5. **Convert**
   - Click "Convert to Audio"
   - Monitor progress in the progress bar
   - Audio files will be saved in the same directory as the script

### File Management

- **Add more files**: Click "Add PDF Files" again to add additional PDFs
- **Remove files**: Select files in the list and click "Remove Selected"
- **Clear all**: Click "Clear All" to remove all files from the list

### Output Modes

#### Separate Files Mode
- Creates individual `.wav` files for each PDF
- Naming format: `[prefix]_[filename].wav`
- Example: `audiobook_chapter1.wav`, `audiobook_chapter2.wav`

#### Combined Mode
- Creates one `.wav` file containing all PDFs
- Adds filename announcements between documents
- Naming format: `[name]_combined.wav`
- Example: `complete_audiobook_combined.wav`

## Voice Settings

### Speech Rate
- Range: 100-300 words per minute (WPM)
- Default: 200 WPM
- Adjust using the slider for comfortable listening speed

### Voice Selection
- Automatically detects available system voices
- Windows: SAPI voices (male/female options)
- macOS: System voices (various languages and genders)
- Linux: espeak/festival voices

## Troubleshooting

### Common Issues

**"No module named 'pyttsx3'"**
```bash
pip install pyttsx3
```

**"No module named 'PyPDF2'"**
```bash
pip install PyPDF2
```

**"No text found in PDF"**
- PDF may contain only images/scanned content
- Try OCR software first to make PDF text-searchable
- Some PDFs have text extraction restrictions

**Audio file not playing**
- Ensure your system has audio codecs for WAV files
- Try playing with different media players
- Check file wasn't corrupted during conversion

**Voice not working on Linux**
```bash
# Install espeak
sudo apt-get install espeak espeak-data

# Or install festival
sudo apt-get install festival
```

### Performance Tips

- **Large PDFs**: Break into smaller files for faster processing
- **Multiple files**: Use separate mode for better error isolation
- **Memory usage**: Close other applications if processing many large files
- **Speed**: Higher speech rates process faster but may affect quality

## File Formats

### Input
- **Supported**: PDF files with extractable text
- **Not supported**: Image-only PDFs, password-protected PDFs

### Output
- **Format**: WAV (uncompressed audio)
- **Quality**: 16-bit, system default sample rate
- **Compatibility**: Plays on all major media players

## Technical Details

### Dependencies
- **pyttsx3**: Text-to-speech conversion
- **PyPDF2**: PDF text extraction
- **tkinter**: GUI framework (included with Python)
- **threading**: Background processing

### Architecture
- Main thread handles GUI responsiveness
- Worker thread processes PDF conversion
- Progress updates via thread-safe callbacks
- Error handling prevents application crashes

## Contributing
Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Potential Improvements
- Add MP3 output support
- OCR integration for image-based PDFs
- Batch processing with job queue
- Audio quality settings
- Pause/resume functionality
- Bookmark support for long documents

## License
- This project is open source. Feel free to use, modify, and distribute as needed.

## Support
For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify PDF files contain extractable text
4. Test with a simple, small PDF first

## Version History
### v2.0
- Added multiple PDF support
- Implemented dual conversion modes
- Enhanced GUI with file management
- Added progress tracking
- Improved error handling

### v1.0
- Basic single PDF conversion
- Simple GUI interface
- Voice selection
- Speech rate adjustment

---

**Enjoy converting your PDFs to audio!** 🎧📚
