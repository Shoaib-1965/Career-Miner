# 🎯 Career-Miner

**A lightweight Python-based job scraper that automatically collects job listings from Indeed and Glassdoor.**

Career-Miner is an intelligent automation tool that searches for jobs based on custom keywords and locations, bypasses Cloudflare protection using undetected Chrome driver, and exports all data into a structured Excel file. It leverages your existing Chrome profile for seamless auto-login to job platforms.

---

## ✨ Features

- 🔍 **Multi-Platform Support** - Scrapes Indeed and Glassdoor simultaneously
- 🌐 **Cloudflare Bypass** - Uses `undetected-chromedriver` to auto-bypass bot detection
- 🔐 **Auto-Login** - Uses your Chrome profile for seamless authentication
- 📊 **Excel Export** - Saves all job data in organized Excel spreadsheets
- 🎯 **Custom Search** - Filter by job title, location, and experience level
- 📧 **Contact Extraction** - Attempts to extract emails, phone numbers, and company info
- ⚡ **Smart Rate Limiting** - Random delays to mimic human behavior
- 🛡️ **Error Handling** - Robust exception handling with detailed logging

---

## 📸 Screenshots

### Indeed Job Scraping
![Indeed Scraping](https://github.com/user-attachments/assets/e3b0dd5e-8401-4cd2-8680-a7cadac0404d)

### Glassdoor Job Search
![Glassdoor Search](https://github.com/user-attachments/assets/18090f3e-096c-4b3e-9a08-21384ff37819)

### Job Listings Results
![Job Results](https://github.com/user-attachments/assets/863377d7-1473-446f-a354-f4b4da423dcc)

### Excel Output
![Excel Export](https://github.com/user-attachments/assets/58d99888-05e9-4d2e-853c-daa387313e8d)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system
- **Google Chrome** browser (latest version recommended)
- **ChromeDriver** matching your Chrome version
- Basic knowledge of command-line operations

---

## 📦 Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/shoaib-altaf/career-miner.git
cd career-miner
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Or install manually:**

```bash
pip install undetected-chromedriver pandas openpyxl selenium
```

### Step 3: Download ChromeDriver

#### Option A: Automatic (Recommended)

The script will attempt to download ChromeDriver automatically on first run.

#### Option B: Manual Download

1. **Check your Chrome version:**
   - Open Chrome → Menu (⋮) → Help → About Google Chrome
   - Note your version (e.g., `131.0.6778.86`)

2. **Download matching ChromeDriver:**
   - Visit: [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/)
   - Download the version matching your Chrome browser
   - Choose your OS: Windows, macOS, or Linux

3. **Extract and place ChromeDriver:**

   **Windows:**
   ```
   C:\Users\YourName\Documents\career-miner\drivers\chromedriver.exe
   ```

   **macOS/Linux:**
   ```
   ~/career-miner/drivers/chromedriver
   ```

4. **Update the path in `scrapper.py`:**

   ```python
   chromedriver_path = r"C:\Users\YourName\Documents\career-miner\drivers\chromedriver.exe"
   ```

### Step 4: Create Chrome Profile Folder

```bash
# Windows
mkdir chrome_profile

# macOS/Linux
mkdir chrome_profile
```

---

## ⚙️ Configuration

### Edit Configuration in `scrapper.py`

Open `scrapper.py` and modify the following settings:

```python
# Job search configuration
JOB_TITLE = "Flutter Developer"  # Change to your desired job title
LOCATION = "Lahore"              # Change to your location
MAX_PAGES = 2                     # Number of pages to scrape per site

# Paths (update these to match your system)
chromedriver_path = r"C:\Users\YourName\Documents\career-miner\drivers\chromedriver.exe"
chrome_profile_path = r"C:\Users\YourName\Documents\career-miner\chrome_profile"
output_folder = r"C:\Users\YourName\Downloads"
```

---

## 🎯 Usage

### Running the Scraper

```bash
python scrapper.py
```

### First-Time Setup

On first run, the script will:

1. Open Chrome with a fresh profile
2. Navigate to Indeed and Glassdoor
3. **You need to manually log in once** on both sites
4. After login, sessions are saved in `chrome_profile` folder
5. Future runs will auto-login using saved sessions

### What Happens During Scraping

1. ✅ Opens undetected Chrome browser
2. ✅ Bypasses Cloudflare verification automatically
3. ✅ Searches for jobs with your specified criteria
4. ✅ Extracts job details (title, company, experience, contact info)
5. ✅ Handles pagination automatically
6. ✅ Saves data to timestamped Excel file

### Output

Excel file will be saved as:
```
flutter_jobs_lahore_20251115_143025.xlsx
```

**Columns in Excel:**
- Source (Indeed/Glassdoor)
- Job Title
- Company Name
- Location
- Required Experience
- Email (if available)
- Phone Number (if available)
- Company Website
- Job URL
- Scraped Date & Time

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **ChromeDriver Version Mismatch**

**Error:** `SessionNotCreatedException: session not created`

**Solution:**
- Check Chrome version: `chrome://version`
- Download matching ChromeDriver
- Update path in script

#### 2. **Chrome Profile Locked**

**Error:** `Chrome instance exited`

**Solution:**
- Close ALL Chrome windows
- Run script again
- Or use a separate profile folder

#### 3. **Cloudflare Blocking**

**Error:** "Additional Verification Required"

**Solution:**
- Wait 10-15 seconds on verification page
- Script uses `undetected-chromedriver` which bypasses most checks
- Ensure you're not scraping too aggressively

#### 4. **No Jobs Found**

**Possible Causes:**
- Incorrect location spelling
- No jobs available for search criteria
- Page structure changed (check selectors)

**Solution:**
- Verify search terms manually on the website
- Check console output for selector errors
- Update selectors if needed

#### 5. **Module Not Found**

**Error:** `ModuleNotFoundError: No module named 'undetected_chromedriver'`

**Solution:**
```bash
pip install undetected-chromedriver
```

---

## 📋 Requirements

```txt
undetected-chromedriver>=3.5.0
selenium>=4.15.0
pandas>=2.0.0
openpyxl>=3.1.0
```

---

## ⚠️ Legal & Ethical Considerations

### Important Disclaimers

- ⚖️ **Terms of Service:** Both Indeed and Glassdoor prohibit automated scraping in their ToS
- 🔒 **Use Responsibly:** This tool is for educational and personal research purposes only
- 🚫 **Do Not:** Use for commercial purposes, mass data collection, or redistribution
- ✅ **Consider Alternatives:** Both sites offer official APIs for legitimate use cases

### Ethical Usage Guidelines

1. Limit scraping frequency (use delays between requests)
2. Respect `robots.txt` directives
3. Do not overload servers with excessive requests
4. Use data for personal job search only
5. Consider using official job board APIs when available

### Recommended Alternatives

- **Indeed Publisher API** - Official API for job data
- **Glassdoor API for Partners** - Partner program access
- **LinkedIn Jobs API** - Legitimate developer access
- Manual job alerts and RSS feeds

**By using this tool, you agree to comply with all applicable laws and terms of service.**

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Shoaib Altaf**

- LinkedIn: [@shoaib-altaf](https://linkedin.com/in/shoaib-altaf)
- GitHub: [@shoaib-altaf](https://github.com/shoaib-altaf)

---



## ⭐ Star This Repository

If you find Career-Miner helpful, please consider giving it a star! It helps others discover the project.

---

**Built with ❤️ by [Shoaib Altaf](https://linkedin.com/in/shoaib-altaf)**

*Last Updated: November 2025*
