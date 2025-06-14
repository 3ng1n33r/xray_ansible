import json
import subprocess
import argparse

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
                    flow = user.get('flow')

            stream_settings = outbound.get('streamSettings', {})

            network = stream_settings.get('network')
            security = stream_settings.get('security')
            reality_settings = stream_settings.get('realitySettings', {})

            fingerprint = reality_settings.get('fingerprint')
            server_name = reality_settings.get('serverName')
            public_key = reality_settings.get('publicKey')
            short_id = reality_settings.get('shortId')
            
            url = protocol+"://"+user_id+"@"+address+":"+str(port)+"?type="+network+"&security="+security+"&sni="+server_name+"&pbk="+public_key+"&flow="+flow+"&sid="+short_id+"&fp="+fingerprint+"#proxy"
            output_file = f"qr-{args.file}.png"
            command = ["qrencode", "-o", output_file, url]
            subprocess.run(command)
        else:
            print("Failed to obtaind data")
except FileNotFoundError:
    print(f"Error: File {args.file} not found")
