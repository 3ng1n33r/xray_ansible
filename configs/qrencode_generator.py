import json
import subprocess
import argparse
import urllib.parse
from urllib.parse import quote

parser = argparse.ArgumentParser(description='This script generates a qr code image based on the Xray-core configuration file')
parser.add_argument('-f','--file', type=str, help='configuration file name', required=True)
args = parser.parse_args()

try:
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)

        outbound = data.get('outbounds', [])[0] if data.get('outbounds') else None

        if outbound:
            protocol = outbound.get('protocol')
            
            vnext = outbound.get('settings', {}).get('vnext', [])
            if vnext:
                vnext_entry = vnext[0]
                address = vnext_entry.get('address')
                port = vnext_entry.get('port')
                
                users = vnext_entry.get('users', [])
                if users:
                    user = users[0]
                    user_id = user.get('id')
                    encryption = user.get('encryption')

            stream_settings = outbound.get('streamSettings', {})
            network = stream_settings.get('network')
            security = stream_settings.get('security')

            # xhttpSettings
            xhttp_settings = stream_settings.get('xhttpSettings', {})
            path = xhttp_settings.get('path', '')

            extra = xhttp_settings.get('extra', {})

            extra_encoded = urllib.parse.quote(
                json.dumps(extra, separators=(',', ':'))
            )

            reality_settings = stream_settings.get('realitySettings', {})
            fingerprint = reality_settings.get('fingerprint')
            server_name = reality_settings.get('serverName')
            public_key = reality_settings.get('publicKey')
            short_id = reality_settings.get('shortId')
            spider_x = reality_settings.get('spiderX', '')

            url = (
                f"{protocol}://{user_id}@{address}:{port}"
                f"?type={network}"
                f"&security={security}"
                f"&sni={server_name}"
                f"&pbk={public_key}"
                f"&encryption={encryption}"
                f"&sid={short_id}"
                f"&spx={quote(spider_x)}"
                f"&fp={fingerprint}"
                f"&path={quote(path)}"
                f"&extra={extra_encoded}"
                f"&mode=auto#{address}"
            )

            print(url)
            output_file = f"qr-{args.file}.png"
            command = ["qrencode", "-o", output_file, url]
            subprocess.run(command)
        else:
            print("Failed to obtaind data")
except FileNotFoundError:
    print(f"Error: File {args.file} not found")
