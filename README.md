<p align="center">
  <img src="https://i.postimg.cc/25PdmsWM/FTP-Hunter-logo.png" alt="FTP-Hunter Logo" width="150">
</p>

<h2 align="center">ＦＴＰ－ＨＵＮＴＥＲ</h2>

<p align="center">
  <b>FTP Hunter is a tool for scanning FTP servers and detecting sensitive files.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0-red" alt="Version">
  <img src="https://img.shields.io/github/issues-closed/xtawb/FTP-Hunter">
</p>

# FTP Hunter

**FTP Hunter** is a powerful and efficient tool designed for scanning FTP servers and detecting sensitive files. It provides a detailed directory tree of the FTP server and highlights potentially sensitive files based on predefined keywords. The tool supports both root and anonymous logins and can handle multiple IP addresses concurrently using multi-threading.

---

## Key Features

- **FTP Server Scanning:** Scan FTP servers for directory structures and files.
- **Sensitive File Detection:** Highlight files that match predefined sensitive keywords (e.g., `password`, `config`, `backup`, etc.).
- **Multi-Threading:** Scan multiple IP addresses concurrently for faster results.
- **Interactive Interface:** User-friendly interface with colored output for better readability.
- **Report Generation:** Save scan results in CSV format for further analysis.
- **Dynamic IP Input:** Users can specify the path to a file containing IP addresses to scan.

---

## Installation

No external libraries are required to run FTP Hunter. It uses Python's standard libraries. Simply clone the repository or download the script.

```bash
git clone https://github.com/xtawb/FTP-Hunter.git
cd FTP-Hunter
```

---

## Usage

1. **Prepare the IP List:**
   Create a file named `ips.txt` (or any name you prefer) and add the IP addresses you want to scan, one per line.

   Example `ips.txt`:
   ```
   192.168.1.1
   192.168.1.2
   192.168.1.3
   ```

   Alternatively, you can extract IP addresses from a webpage (e.g., Shodan) using the JavaScript code provided below.

2. **Run the Tool:**
   Execute the script using Python 3.

   ```bash
   python tool.py
   ```

3. **Enter the Path to the IP File:**
   When prompted, enter the path to your `ips.txt` file (or the file containing the IP addresses).

   ```
   Enter the path to the IPs file (e.g., ips.txt): ips.txt
   ```

4. **View Results:**
   The tool will display the directory tree of each FTP server it successfully logs into. Sensitive files will be highlighted in red.

5. **Generated Files:**
   - **successful_ips.txt:** Contains a list of IP addresses where the login was successful.
   - **ftp_report.csv:** Contains a detailed report of the scan, including the IP address, login type, directory tree, and timestamp.

---

## Extracting IP Addresses from Shodan

You can use the following JavaScript code to extract all IP addresses from a webpage (e.g., Shodan) and download them as a text file (`ips.txt`).

### JavaScript Code to Extract All IP Addresses from a Webpage and Download Them as `ips.txt`

This script scans an entire webpage for **any IP addresses** and then **downloads them as a text file (`ips.txt`)**.

---

🔹 **JavaScript Code:**  
```javascript
// Extract all text content from the webpage
let pageText = document.body.innerText;

// Regular expression to find all IP addresses
let ipRegex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/g;
let ips = pageText.match(ipRegex) || []; // Get all matches or return an empty array if no IPs are found

// Remove duplicate IPs
ips = [...new Set(ips)];

// Check if any IPs were found
if (ips.length === 0) {
    console.error("❌ No IP addresses found on this page!");
} else {
    // Convert the IP list to a text file
    let blob = new Blob([ips.join("\n")], { type: "text/plain" });

    // Create a download link
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ips.txt"; // Filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    console.log("✅ File 'ips.txt' has been downloaded successfully! It contains " + ips.length + " IP addresses.");
}
```

---

### 📌 **How to Use This Code on Shodan (Step-by-Step Guide)**  

1️ **Go to [Shodan](https://www.shodan.io/)** and log in to your account.  
2️⃣ **Search for anything** (e.g., port:21 "220" "230 Login successful." country:"US".).  
3️⃣ **Once the results are displayed**, press `F12` to open **Developer Tools**.  
4️⃣ Go to the **Console** tab.  
5️⃣ Type `allow pasting` and Copy and paste the JavaScript code above into the Console.  
6️⃣ Press `Enter` to execute the script.  
7️⃣ A file named **`ips.txt`** will be automatically downloaded, containing all IP addresses found on the page.  

![🔗 JavaScript Code Image](https://i.postimg.cc/Jh4700NB/ips-auto.png)

🔹 **Why This Code is Useful?**  
✔ **Extracts all IP addresses dynamically** from the entire webpage.  
✔ **Works on any website** (not just Shodan).  
✔ **Filters out duplicate IPs** automatically.  
✔ **Generates and downloads the file automatically**—no manual copying required.

---

## Example Output

### Banner
```
███████╗████████╗██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
█████╗     ██║   ██████╔╝█████╗███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══╝     ██║   ██╔═══╝ ╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║        ██║   ██║           ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝        ╚═╝   ╚═╝           ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

Version: v1.0
Description: FTP Hunter is a tool for scanning FTP servers and detecting sensitive files.
Contact: https://linktr.ee/xtawb
Github : https://github.com/xtawb
```
![🔗 Example Output Image](https://i.postimg.cc/tCMYLhWm/FTP-Hunter-tool.png)

### Scan Results
```
[*] Number of IPs to scan: 3

[+] Server: 192.168.1.1
[+] Root Login Successful!

Directory Tree:
├── public_html
│   ├── index.html
│   └── config.php
└── logs
    └── access.log

[+] Server: 192.168.1.2
[+] Anonymous Login Successful!

Directory Tree:
├── pub
│   └── README.txt
└── secret
    └── credentials.txt

[*] Scan completed!
[+] Successful logins: 2
[-] Failed logins: 1
[+] Successful IPs saved to successful_ips.txt
[+] Report saved to ftp_report.csv
```
![🔗 Scan Results Image](https://i.postimg.cc/BnFQkRqX/FTP-Hunter-work.png)

![🔗 Scan Results Image](https://i.postimg.cc/DZS2QNYv/FTP-Hunter-work2.png)

---

## Keywords

The tool highlights files that match the following sensitive keywords:

- `password`
- `config`
- `backup`
- `secret`
- `.sql`
- `.env`
- `.png`
- `.jpg`
- `.mp3`
- `.mp4`
- `credentials`

You can modify the `sensitive_keywords` list in the script to add or remove keywords.

---

## Requirements

- Python 3.x
- No external libraries required.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or suggestions, feel free to reach out:

- **Contact:** [https://linktr.ee/xtawb](https://linktr.ee/xtawb)
- **GitHub:** [https://github.com/xtawb](https://github.com/xtawb)

---

## Keywords (for SEO)

- FTP Scanner
- FTP Server
- Sensitive File Detection
- FTP Security
- FTP Hunter
- FTP Tool
- Python FTP Scanner
- Multi-threaded FTP Scanner
- FTP Directory Tree
- FTP Report Generator
