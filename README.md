```markdown
# WAC - WiFi Admin Cracker 🔓

A powerful and efficient WiFi router admin panel penetration testing tool designed for security assessments and authorized testing.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2FLinux%2FmacOS-lightgrey.svg)

## 🚀 Features

- **High-Speed Cracking**: Multi-threaded architecture for maximum efficiency
- **Auto Form Detection**: Automatically identifies login form fields
- **Comprehensive Wordlists**: Pre-loaded with 1000+ default credentials
- **Stealth Mode**: Minimal network footprint during scanning
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **No Dependencies**: Pure Python - no external libraries required

## 📋 Prerequisites

- Python 3.6 or higher
- Network access to target router
- Authorization to test the target

## ⚡ Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/crow-sefeshki/Wifi-Admin_Cracker.git
cd Wifi-Admin_Cracker
```

2. **Run the tool**
```bash
python wac_cracker.py
```

3. **Enter target IP when prompted**
```
Enter router IP or URL: 192.168.1.1
```

## 🛠️ Usage

### Basic Usage
```bash
python wac_cracker.py
```

### Target Formats
- IP address: `192.168.1.1`
- URL: `http://router.local`
- With port: `192.168.1.1:8080`

### Required Files
- `user.txt` - Contains username wordlist
- `pswrd.txt` - Contains password wordlist

## 📁 File Structure

```
Wifi-Admin_Cracker/
├── wac_cracker.py      # Main tool
├── user.txt           # Username wordlist
├── pswrd.txt          # Password wordlist
├── README.md          # This file
└── LICENSE            # MIT License
```

## 🎯 How It Works

1. **Target Analysis**: Automatically detects login form structure
2. **Field Identification**: Identifies username and password fields
3. **Credential Testing**: Tests all combinations from wordlists
4. **Success Detection**: Analyzes responses for successful login indicators
5. **Results Display**: Shows compromised credentials instantly

## 📊 Default Credentials Database

The tool includes extensive wordlists covering:

- **Vendor Defaults**: Cisco, TP-Link, D-Link, Netgear, ASUS, Linksys, etc.
- **Common Combinations**: admin/admin, admin/password, root/1234, etc.
- **Regional Defaults**: Common credentials by region and ISP
- **Blank Credentials**: Empty username/password combinations

## ⚠️ Legal Disclaimer

This tool is intended for:
- Security research and education
- Authorized penetration testing
- Testing your own equipment
- Cybersecurity training

**⚠️ WARNING**: Unauthorized use against networks you don't own is illegal. The developer is not responsible for misuse. Always ensure you have explicit permission before testing.

## 🛡️ Responsible Disclosure

If you discover vulnerabilities using this tool:
1. Report them to the vendor
2. Follow responsible disclosure practices
3. Help improve network security

## 🔧 Customization

### Adding Custom Credentials
Edit `user.txt` and `pswrd.txt` files:
```bash
# Add to user.txt
custom_admin
superuser
technician

# Add to pswrd.txt
Company123!
P@ssw0rd2024
SecurePass!
```

### Modifying Thread Count
Edit the `max_workers` parameter in `wac_cracker.py`:
```python
with ThreadPoolExecutor(max_workers=50) as executor:
```

## 📈 Performance

- **Speed**: Tests 1000+ combinations per minute
- **Efficiency**: Low resource consumption
- **Reliability**: Accurate success detection
- **Stealth**: Minimal log generation

## 🐛 Troubleshooting

### Common Issues

**"Connection refused"**
- Check target IP/URL
- Verify network connectivity
- Ensure target is accessible

**"No credential files"**
- Verify `user.txt` and `pswrd.txt` exist
- Check file permissions
- Ensure files are in same directory

**"Form detection failed"**
- Target may use JavaScript
- Try manual field configuration
- Check for custom login mechanisms

## 📞 Contact

- **Developer**: crow
- **Telegram**: [@sefeshki](https://t.me/sefeshki)
- **GitHub**: [crow-sefeshki](https://github.com/crow-sefeshki)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**⚠️ OWNERSHIP NOTICE**: This tool is the exclusive property of crow (@sefeshki). Unauthorized redistribution, claiming of authorship, or commercial use without permission is strictly prohibited.

**⭐ If you find this tool useful, please give it a star!**
```
