#!/usr/bin/env python3
"""
Simple Flask OAuth Callback Server

A lightweight Flask app that listens for OAuth callbacks and displays the authorization code
in a nicely formatted HTML page. Runs on HTTPS with a self-signed certificate.

Usage:
    python oauth_callback_flask.py

The server will start on https://localhost:8443/oauth_callback
"""

import os
import ssl
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for displaying the OAuth response
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OAuth Callback</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        .success {
            color: #28a745;
            font-size: 48px;
            margin-bottom: 20px;
        }
        .error {
            color: #dc3545;
            font-size: 48px;
            margin-bottom: 20px;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .code-container {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }
        .code-label {
            font-weight: bold;
            color: #495057;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .code-value {
            font-size: 16px;
            color: #212529;
            background: white;
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #dee2e6;
            user-select: all;
        }
        .instructions {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            color: #1565c0;
            font-size: 14px;
        }
        .copy-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 5px;
            font-size: 14px;
            transition: background-color 0.3s;
        }
        .copy-btn:hover {
            background: #0056b3;
        }
        .error-details {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
            text-align: left;
        }
        .footer {
            margin-top: 30px;
            color: #6c757d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if success %}
            <div class="success">✅</div>
            <h1>OAuth Authorization Successful!</h1>
            
            <div class="instructions">
                <strong>📋 Copy the authorization code below and paste it into your application:</strong>
            </div>
            
            <div class="code-container">
                <div class="code-label">Authorization Code:</div>
                <div class="code-value" id="authCode">{{ auth_code }}</div>
            </div>
            
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy Code</button>
            
            {% if state %}
            <div class="code-container">
                <div class="code-label">State Parameter:</div>
                <div class="code-value">{{ state }}</div>
            </div>
            {% endif %}
            
        {% else %}
            <div class="error">❌</div>
            <h1>OAuth Authorization Failed</h1>
            
            <div class="error-details">
                <strong>Error:</strong> {{ error_type }}<br>
                <strong>Description:</strong> {{ error_description }}
            </div>
            
            <div class="instructions">
                Please check your OAuth configuration and try again. Make sure your client ID and redirect URI are correctly configured.
            </div>
            
        {% endif %}
        
        <div class="footer">
            OFC • {{ timestamp }}
        </div>
    </div>

    <script>
        function copyToClipboard() {
            const codeElement = document.getElementById('authCode');
            const textArea = document.createElement('textarea');
            textArea.value = codeElement.textContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            // Show feedback
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = '✅ Copied!';
            button.style.background = '#28a745';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '#007bff';
            }, 2000);
        }
        
        // Auto-select code on click
        document.getElementById('authCode')?.addEventListener('click', function() {
            window.getSelection().selectAllChildren(this);
        });
    </script>
</body>
</html>
"""


@app.route('/oauth_callback', methods=['GET'])
def oauth_callback():
    """Handle OAuth callback and display the authorization code."""
    
    # Get query parameters
    auth_code = request.args.get('code')
    error = request.args.get('error')
    error_description = request.args.get('error_description', 'No description provided')
    state = request.args.get('state')
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if auth_code:
        # Success case
        print(f"✅ OAuth callback received - Authorization Code: {auth_code[:10]}...{auth_code[-10:]}")
        return render_template_string(
            HTML_TEMPLATE,
            success=True,
            auth_code=auth_code,
            state=state,
            timestamp=timestamp
        )
    elif error:
        # Error case
        print(f"❌ OAuth error received - {error}: {error_description}")
        return render_template_string(
            HTML_TEMPLATE,
            success=False,
            error_type=error,
            error_description=error_description,
            timestamp=timestamp
        )
    else:
        # No code or error - invalid request
        print("⚠️ Invalid OAuth callback - no code or error parameter")
        return render_template_string(
            HTML_TEMPLATE,
            success=False,
            error_type="Invalid Request",
            error_description="No authorization code or error parameter found in the callback URL",
            timestamp=timestamp
        )


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with instructions."""
    # Get the host URL for dynamic endpoint display
    host = request.host_url
    return f"""
    <html>
    <head>
        <title>OAuth Callback Server</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .endpoint {{ background: #e3f2fd; padding: 15px; border-radius: 5px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 OAuth Callback Server</h1>
            <p>This Flask server is running and ready to receive OAuth callbacks.</p>
            
            <h3>📡 Callback Endpoint:</h3>
            <div class="endpoint">
                <strong>{host}oauth_callback</strong>
            </div>
            
            <h3>📋 Usage:</h3>
            <ol>
                <li>Configure your OAuth application to use the callback URL above</li>
                <li>Start your OAuth flow</li>
                <li>After authorization, the code will be displayed here</li>
            </ol>
        </div>
    </body>
    </html>
    """


def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS."""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import ipaddress
        
        # Create certs directory if it doesn't exist
        certs_dir = os.path.join(os.path.dirname(__file__), 'certs')
        os.makedirs(certs_dir, exist_ok=True)
        
        cert_path = os.path.join(certs_dir, 'localhost.crt')
        key_path = os.path.join(certs_dir, 'localhost.key')
        
        # Check if certificates already exist and are still valid
        if os.path.exists(cert_path) and os.path.exists(key_path):
            try:
                # Check if certificate is still valid (not expired)
                with open(cert_path, 'rb') as cert_file:
                    cert_data = cert_file.read()
                    cert = x509.load_pem_x509_certificate(cert_data)
                    # Use the non-deprecated UTC method if available, fallback to the old method
                    if hasattr(cert, 'not_valid_after_utc'):
                        expiry = cert.not_valid_after_utc
                        now = datetime.now(expiry.tzinfo) if expiry.tzinfo else datetime.utcnow()
                    else:
                        expiry = cert.not_valid_after
                        now = datetime.utcnow()
                    
                    if expiry > now:
                        print("✅ Using existing SSL certificate")
                        return cert_path, key_path
            except Exception:
                # If there's any error reading the cert, we'll regenerate
                pass
        
        print("🔧 Generating new SSL certificate...")
        
        # Generate private key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate (valid for 30 days)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"OAuth Callback Server"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=30)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.IPAddress(ipaddress.IPv4Address(u"127.0.0.1")),
                x509.DNSName(u"localhost"),
            ]),
            critical=False,
        ).sign(key, hashes.SHA256())
        
        # Write certificate and key to persistent files
        with open(cert_path, 'wb') as cert_file:
            cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(key_path, 'wb') as key_file:
            key_file.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print(f"✅ SSL certificate saved to {certs_dir}/")
        return cert_path, key_path
        
    except ImportError:
        print("⚠️ cryptography library not found. Install it with: pip install cryptography")
        print("⚠️ Falling back to HTTP (not HTTPS)")
        return None, None


if __name__ == '__main__':
    print("🚀 Starting OAuth Callback Server...")
    print("="*50)
    
    # Try to create SSL certificate
    cert_path, key_path = create_self_signed_cert()
    
    if cert_path and key_path:
        # HTTPS mode
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)
        
        print("✅ HTTPS server starting...")
        print("📡 Callback URL: https://localhost:8443/oauth_callback")
        print("🌐 Server info: https://localhost:8443/")
        print("")
        print("⚠️  Browser may show security warnings (self-signed certificate)")
        print("   Click 'Advanced' → 'Proceed to localhost (unsafe)' if prompted")
        print("")
        print("📋 Use this URL in your OAuth application redirect URI:")
        print("   https://localhost:8443/oauth_callback")
        print("")
        print("🛑 Press Ctrl+C to stop the server")
        print("="*50)
        
        app.run(host='0.0.0.0', port=8443, ssl_context=context, debug=False)
    else:
        # HTTP fallback
        print("⚠️ Running in HTTP mode (no SSL)")
        print("📡 Callback URL: http://localhost:8443/oauth_callback")
        print("🌐 Server info: http://localhost:8443/")
        print("")
        print("📋 Use this URL in your OAuth application redirect URI:")
        print("   http://localhost:8443/oauth_callback")
        print("")
        print("🛑 Press Ctrl+C to stop the server")
        print("="*50)
        
        app.run(host='0.0.0.0', port=8443, debug=False)
