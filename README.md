<p align="center">
  <img src="assets/logo.svg" width="420" alt="BROsint Logo">
</p>

## 🕵️ BROsint

> **Advanced OSINT framework for phone, email, and social footprint reconnaissance — built for ethical cybersecurity research.**

**Author:** Chinedu • **Version:** 1.0.0

```

██████╗ ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
██╔══██╗██╔══██╗██╔════╝ ██╔════╝██║████╗  ██║╚══██╔══╝
██████╔╝██████╔╝██║  ███╗█████╗  ██║██╔██╗ ██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║╚██╗██║   ██║
██║     ██║  ██║╚██████╔╝██║     ██║██║ ╚████║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝

```

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Built%20with-Python-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📖 Overview

**BROsint** is a free, fully interactive OSINT (Open Source Intelligence) tool that empowers ethical investigators, researchers, and security enthusiasts to perform advanced intelligence collection.

It can investigate emails, usernames, phone numbers, domains, and files with live results fetched directly from the internet. BROsint's dynamic neon web dashboard gives you real-time results, AI-generated hypotheses, and supports Google dorking for deeper web discovery.

---

## ✨ Features

| Category | Capabilities |
|----------|--------------|
| **Identity Intelligence** | Email, username, and phone lookup with real-time results |
| **Domain Intelligence** | WHOIS lookup and IP geolocation |
| **File Analysis** | EXIF metadata extraction from images and documents |
| **AI-Powered Analysis** | Hypothesis generation and confidence scoring |
| **Deep Web Discovery** | Google dork support for advanced intelligence gathering |
| **Interactive Dashboard** | Neon‑styled web interface with live search and results |
| **Visual Design** | Professional neon ASCII art for a futuristic aesthetic |

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/anonymous-beta/Brosint.git
cd Brosint

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the web interface
python brosint.py --web
```

Once running, access the dashboard at: http://127.0.0.1:5000

---

## 🚀 Usage

Command‑Line Examples

```bash
# Email intelligence
python brosint.py --email example@mail.com

# Username analysis
python brosint.py --username exampleuser

# Domain lookup
python brosint.py --domain example.com

# Run with web interface
python brosint.py --web
```

## What You Get

· Email traces and patterns
· Domain and WHOIS data
· File metadata (EXIF)
· AI‑generated hypotheses and confidence levels

Results can be exported or shared directly from the dashboard.

---

## 📝 Notes

· BROsint uses only publicly available information — it does not access private databases or paid APIs
· Completely free and open‑source — designed for learning, research, and ethical use
· Built for Termux, Linux, and other Unix‑like environments
· The web interface features neon dynamic visuals with interactive elements powered by Flask

---

## 🤝 Contributing

BROsint welcomes community contributions!

1. Fork the repo
2. Make your changes
3. Commit: git commit -m "Add new feature"
4. Push to your fork: git push origin main
5. Open a pull request for review

Contributions can include:

· Bug fixes
· New OSINT modules
· UI improvements

---

## 📄 License

This project is licensed under the MIT License.

⚠️ Use responsibly — this software is intended for educational and ethical use only. Misuse for illegal surveillance or privacy violations is strictly forbidden.

---

© 2026 Chinedu. All Rights Reserved.
