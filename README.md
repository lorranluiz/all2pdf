# 📄 All2PDF Converter

A powerful command-line tool that automatically converts various document formats to PDF.

## 📋 Table of Contents
- [What Is This?](#-what-is-this)
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [How to Use](#-how-to-use)
- [Support This Project](#-support-this-project)
- [Contact](#-contact)

## 🤔 What Is This?
All2PDF is a lightweight, yet powerful Python utility that scans a directory and automatically converts text files (.txt), Word documents (.doc, .docx) to PDF format. It's designed to be simple, fast, and efficient, running directly from your terminal on Ubuntu or Windows with WSL.

## ✨ Features
- 🔄 **Batch Conversion**: Automatically detects and converts multiple files at once
- 📊 **Progress Bar**: Visual feedback on conversion progress
- 🔍 **Smart Detection**: Automatically identifies file types and uses the appropriate conversion method
- 🛠️ **Versatile**: Works with .txt, .doc, and .docx files
- 📦 **Dependency Management**: Automatically handles dependencies or uses system tools when available
- 🖥️ **Cross-Platform**: Works on Ubuntu and Windows (via WSL)
- 🧩 **Right-Click Integration**: Windows installer adds context menu integration

## 💻 System Requirements
- **Ubuntu**: Python 3.6+
- **Tools & Dependencies**:
  - LibreOffice (for DOC/DOCX conversion)
  - enscript & ghostscript (for TXT conversion)
  - Python packages: tqdm, fpdf, docx2pdf, python-docx
- **Windows**: WSL with Ubuntu installed

## 📚 How to Use

### Ubuntu Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/all2pdf.git
cd all2pdf

# Make the script executable
chmod +x all2pdf.py

# Create a symbolic link (optional)
sudo ln -s "$(pwd)/all2pdf.py" /usr/local/bin/all2pdf

# Install dependencies
sudo apt install -y libreoffice-writer enscript ghostscript
```

### Windows Installation
```powershell
# Run the installer as Administrator
.\install.ps1
```

### Basic Usage
```bash
# Convert all supported files in the current directory
all2pdf

# Convert all supported files in a specific directory
all2pdf /path/to/directory
```

### Windows Right-Click Menu
After installation, simply right-click in any folder and select "Executar all2pdf" to convert all supported files in that directory.

## 💖 Support This Project
This project is open-source and built with dedication to help the community. If you find it useful and would like to support its development, consider making a donation. Your support helps keep this project alive and evolving! 🚀

🔹 Ways to support:
- GitHub Sponsors: [![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/lorranluiz)
- Pix (Brazil): 21997427600

Every contribution, big or small, makes a difference. Thank you for your support! 💙

## 📧 Contact
If you have any questions, please raise an issue or contact us at lorranluiz@id.uff.br.
