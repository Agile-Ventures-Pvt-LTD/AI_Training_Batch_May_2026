# -*- coding: utf-8 -*-
import http.server
import socketserver
import webbrowser
import os
import sys
import json
import urllib.parse

from agent_engine import get_sku_details, process_copilot_query, SupervisorAgent
from elevenlabs_service import generate_speech_b64

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Disable caching for live CSV reload
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/sku":
            query_params = urllib.parse.parse_qs(parsed.query)
            sku_id = query_params.get("id", ["SLP-BAM-01"])[0]
            sku_data = get_sku_details(sku_id)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(sku_data).encode("utf-8"))
            return
            
        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, api-key')
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"
        
        try:
            body = json.loads(body_bytes.decode('utf-8'))
        except Exception:
            body = {}
            
        if parsed.path == "/api/chat":
            prompt = body.get("message", "Executive Summary")
            response_data = process_copilot_query(prompt)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        elif parsed.path == "/api/voice-briefing":
            # Generate summary text from SupervisorAgent
            sup = SupervisorAgent()
            res = sup.run_pipeline()
            summary_text = res["consolidated"]["analytics"]["executive_summary"]
            
            audio_b64 = generate_speech_b64(summary_text)
            out_resp = {
                "status": "success" if audio_b64 else "fallback",
                "audio_b64": audio_b64 or "",
                "text": summary_text
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(out_resp).encode("utf-8"))
            return
            
        elif parsed.path == "/api/send-email":
            from email_service import send_executive_briefing_email
            email_addr = body.get("email", "taniya.gupta@agileventures.net")
            metrics = body.get("metrics", None)
            html_content_override = body.get("htmlContent", None)
            res = send_executive_briefing_email(recipient_email=email_addr, metrics_summary=metrics, html_content_override=html_content_override)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return
            
        self.send_response(404)
        self.end_headers()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("==================================================")
    print(f"Sleepsia Executive Hub Local Web Server Started")
    print(f"URL: http://localhost:{PORT}/index.html")
    print("==================================================")
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()

