# 🌐 DNS Analyzer Tool

A desktop-based DNS performance analysis tool built using Python.  
It benchmarks multiple DNS servers, visualizes latency, and provides exportable reports.

---

## ✨ Features

- DNS latency benchmarking (Google, Cloudflare, OpenDNS, Quad9)
- Real-time performance analysis
- Interactive bar graph visualization
- Dark / Light theme support
- Custom DNS server input
- Fastest DNS detection
- System DNS change support (admin required)
- Export results:
  - PDF report
  - CSV file
  - Excel file

---

## 🧠 How It Works

The tool measures DNS response time by establishing a socket connection to port 53 and calculating round-trip latency.

---

## 📊 Export Options

- PDF summary report
- CSV structured data
- Excel spreadsheet

---

## 🖥️ UI Overview

- Modern Tkinter-based interface
- Theme-aware components
- Responsive layout
- Live status logs
- Embedded matplotlib graph visualization

---

## 🔐 Permissions

Changing system DNS requires administrator privileges (Windows).

---

## 🛠️ Tech Stack

- Python
- Tkinter
- Matplotlib
- ReportLab
- OpenPyXL
- Socket Programming

---

## 📁 Project Structure

- `main.py` → Core application
- `requirements.txt` → Dependencies
- `.gitignore` → Ignored files configuration

