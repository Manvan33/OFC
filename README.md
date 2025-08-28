# OFC - OAuth Flask Callback

A simple, single-file Flask application that provides an HTTPS OAuth callback endpoint for OAuth flows. This server displays the authorization code in a beautifully formatted HTML page, making it easy to copy and use in your OAuth authentication process.

## Features

- 🔒 **HTTPS Support**: Uses self-signed certificates for secure callback handling
- 🎨 **Beautiful UI**: Clean, modern HTML interface with copy-to-clipboard functionality
- 📋 **Easy Code Display**: Authorization codes are clearly displayed and easy to copy
- ⚠️ **Error Handling**: Proper display of OAuth errors and descriptions
- 📱 **Responsive**: Works on desktop and mobile browsers
- 🚀 **Single File**: Everything you need in one Python file

## Usage

### 1. Start the Server

```bash
# Using uv (recommended)
uv run python main.py

# Or with regular Python (if Flask is installed)
python3 main.py
```

### 2. Server Information

The server will start and display:
```
🚀 Starting OAuth Callback Server...
✅ HTTPS server starting...
📡 Callback URL: https://localhost:8443/oauth_callback
🌐 Server info: https://localhost:8443/
```

### 3. Configure Your OAuth Application

Use this callback URL in your OAuth application:
```
https://localhost:8443/oauth_callback
```

### 4. Handle Browser Security Warnings

Since the server uses self-signed certificates, your browser will show security warnings:
1. Click **"Advanced"**
2. Click **"Proceed to localhost (unsafe)"**
3. The callback page will load normally

### 5. Copy the Authorization Code

When your OAuth flow completes:
1. The authorization code will be displayed in a formatted box
2. Click the **"📋 Copy Code"** button to copy it to your clipboard
3. Paste the code into your application

## Endpoints

- **`/`** - Server information and status page
- **`/oauth_callback`** - OAuth callback endpoint that handles:
  - Success: `?code=AUTH_CODE&state=STATE`
  - Error: `?error=ERROR_TYPE&error_description=DESCRIPTION`

## Dependencies

- **Flask** - Web framework
- **cryptography** - For self-signed certificate generation (optional)

## Security Notes

- ⚠️ This server uses self-signed certificates, which will trigger browser warnings
- 🔒 The server only runs on localhost and is intended for development use
- 🚫 Do not use this server in production environments
- 💾 No data is stored or logged beyond console output

## Integration with OAuth Flow

This server is designed to work with the simplified OAuth authentication in this project:

1. Start the Flask callback server
2. Run your OAuth flow with `--oauth` flag
3. The authorization URL will open in your browser
4. After authorization, you'll be redirected to the Flask server
5. Copy the displayed code and paste it into your application

## Example Output

**Success Page:**
```
✅ OAuth Authorization Successful!

📋 Copy the authorization code below and paste it into your application:

Authorization Code: [formatted code display with copy button]
```

**Error Page:**
```
❌ OAuth Authorization Failed

Error: access_denied
Description: User denied the request
```

## Troubleshooting

**"Module not found" errors:**
```bash
# Install dependencies
uv add flask cryptography

# Or use uv run
uv run python main.py
```

**Port already in use:**
- Stop any existing servers on port 8443
- Or modify the port in the script

**Browser security warnings:**
- This is normal for self-signed certificates
- Click "Advanced" → "Proceed to localhost"
- The warnings don't affect functionality
