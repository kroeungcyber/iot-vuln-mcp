# Finding Claude Desktop Configuration Directory on macOS

## Method 1: Using Finder (Easiest)

1. Open **Finder**
2. In the menu bar, click **Go** → **Go to Folder...**
3. Type exactly: `~/Library/Application Support/Claude`
4. Press **Go**

## Method 2: Using Terminal

1. Open **Terminal** (you can find it in Applications → Utilities)
2. Run this command:
   ```bash
   open ~/Library/Application\ Support/Claude
   ```
   This will open the Claude folder in Finder.

## Method 3: Alternative Paths to Try

If the above doesn't work, try these paths in Finder's "Go to Folder...":

- `~/Library/Application Support/`
- `~/Library/`
- `/Users/kroeung/Library/Application Support/Claude`

## Method 4: Create the Directory Manually

If the Claude folder doesn't exist yet:

1. Open **Terminal**
2. Run these commands:
   ```bash
   mkdir -p ~/Library/Application\ Support/Claude
   cd ~/Library/Application\ Support/Claude
   ```
3. Then create the config file:
   ```bash
   cat > claude_desktop_config.json << 'EOF'
   {
     "mcpServers": {
       "iot-security-scanner": {
         "command": "docker",
         "args": ["run", "-i", "--rm", "iot-security-scanner"]
       }
     }
   }
   EOF
   ```

## Method 5: Check if Claude Desktop is Installed

Make sure Claude Desktop is actually installed:
- Look for "Claude" in your Applications folder
- If not installed, download it from: https://claude.ai/desktop

## Quick Verification

After creating the config file, you can verify it exists with:
```bash
ls -la ~/Library/Application\ Support/Claude/
```

You should see `claude_desktop_config.json` in the output.

## Troubleshooting

- **Library folder is hidden by default** - Use Method 1 or 2 above
- **Claude folder doesn't exist** - Use Method 4 to create it
- **Still can't find it** - Claude Desktop might not be installed yet

Once you've created the config file and restarted Claude Desktop, you should be able to use the IoT security scanner tools!
