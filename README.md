# 🛡️ Smart Home Security Scanner

> **Check your smart devices for security problems - just by talking to Claude!**

[![Easy to Use](https://img.shields.io/badge/User-Friendly-✅-brightgreen)]()
[![AI Powered](https://img.shields.io/badge/AI--Powered-🤖-blue)]()
[![Legal & Safe](https://img.shields.io/badge/Legal--Compliant-⚖️-important)]()

## 🤔 What Does This Do?

### In Simple Terms:
This tool helps you **find security problems** in your smart home devices like:
- **Security cameras** 📹
- **Smart doorbells** 🚪  
- **Smart thermostats** 🌡️
- **Wi-Fi routers** 📡
- **Any device connected to your home network**

### Why You Need This:
- **80% of smart devices** have security problems out of the box
- **Hackers can access** your cameras and microphones
- **Your personal data** might be exposed
- **You could be watched** without knowing it

### How It Works:
Instead of being a technical expert, you just **talk to Claude** like:
- "Check my security camera at 192.168.1.100"
- "Scan my smart thermostat for problems"  
- "Are my home devices secure?"

## 🚀 Get Started in 3 Easy Steps

### Step 1: Install Docker
**What is Docker?** It's like a secure box that runs the scanner safely.

**Install it here:** https://www.docker.com/products/docker-desktop/

### Step 2: Build the Scanner
Open **Terminal** (Mac) or **Command Prompt** (Windows) and type:

```bash
# Download and build the security scanner
docker build -t iot-security-scanner .
```

### Step 3: Connect to Claude
**For Mac Users:**
1. Open **Finder** → Go to **Home** folder (Press `Cmd+Shift+H`)
2. Go to **Library** → **Application Support** → **Claude**
3. Create/edit `claude_desktop_config.json` with this:

```json
{
  "mcpServers": {
    "iot-security-scanner": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "iot-security-scanner"]
    }
  }
}
```

**For Windows Users:**
1. Press `Win+R`, type `%APPDATA%\Claude` and press Enter
2. Create/edit `claude_desktop_config.json` with the same content above

### Step 4: Restart Claude Desktop
Close and reopen Claude Desktop. You're ready!

## 💬 How to Use (Just Talk!)

### Simple Examples:
```
"Scan my security camera at 192.168.1.100"
"Check if my smart devices have default passwords"
"Test my home network for security problems"
"Analyze my IP camera for vulnerabilities"
```

### What It Checks:
- 🔐 **Default passwords** (like "admin/admin")
- 📹 **Unprotected video streams**
- 🔄 **Outdated software**
- 🌐 **Open network ports**
- 🔍 **Security camera brands** (Hikvision, Dahua, Axis, etc.)

## 🎯 Who Is This For?

### Perfect For:
- **🏠 Homeowners** worried about smart device security
- **👨‍💼 Small business owners** with security cameras
- **👩‍💻 Tech-curious people** who want to learn
- **🏢 Office managers** with IoT devices

### Not For:
- ❌ Scanning devices you don't own
- ❌ Testing neighbors' cameras  
- ❌ Hacking or illegal activities

## ⚠️ Important Legal Notice

### Only Test What You Own!
- ✅ **Your own devices** - Yes!
- ✅ **Devices you manage** - With permission!
- ❌ **Neighbors' cameras** - No!
- ❌ **Public cameras** - No!
- ❌ **Work devices** - Only with written permission!

### Why This Matters:
- **Illegal scanning** can get you in serious trouble
- **Respect privacy** - cameras are private spaces
- **Follow the law** - different countries have different rules

## 🔧 Technical Details (For Curious Minds)

### What's Inside:
- **Security Tools**: Professional-grade scanning tools
- **AI Integration**: Talks to Claude through MCP protocol
- **Safe Container**: Runs in isolated Docker environment
- **No Root Access**: Can't harm your system
- **Rate Limited**: Won't overload your network

### Supported Devices:
- **Security Cameras**: Hikvision, Dahua, Axis, Uniview
- **Smart Home**: Thermostats, doorbells, lights, plugs
- **Network Devices**: Routers, switches, access points

## 🆘 Need Help?

### Common Issues:
- **"Docker not found"** → Install Docker Desktop first
- **"Claude can't connect"** → Restart Claude after config changes
- **"Scanner not working"** → Check your device IP addresses

### Getting Support:
- Check the troubleshooting guide
- Ask in our community forum
- Contact support for professional help

## 📊 What You'll Learn

After scanning, you'll know:
- ✅ Which devices have security problems
- 🔧 How to fix common issues
- 🛡️ How to make your home network safer
- 📈 Your overall security score

---

**Ready to secure your smart home? Just ask Claude to scan your devices!**

> *"Better safe than sorry - know your devices are secure before someone else does."*
