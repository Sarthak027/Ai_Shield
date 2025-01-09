from scapy.all import sniff, Raw
import scapy.all as scapy
from scapy.layers.http import HTTPRequest, HTTP
from scapy.layers.inet import IP, TCP
from scapy.sessions import IPSession, TCPSession
import urllib.parse
from request import Request, DBController
from classifier import ThreatClassifier
from argparse import ArgumentParser

# Update the parser to accept '--port' and '--iface' arguments
parser = ArgumentParser()
parser.add_argument('--port', type=int, default=5000, help='Defines which port to sniff')
parser.add_argument('--iface', type=str, default='Wi-Fi', help='Defines the network interface to sniff on')

args = parser.parse_args()

scapy.packet.bind_layers(TCP, HTTP, dport=args.port)
scapy.packet.bind_layers(TCP, HTTP, sport=args.port)

db = DBController()
threat_clf = ThreatClassifier()

header_fields = ['Http_Version', 'A_IM', 'Accept', 'Accept_Charset', 'Accept_Datetime', 'Accept_Encoding',
                 'Accept_Language', 'Access_Control_Request_Headers', 'Access_Control_Request_Method',
                 'Authorization', 'Cache_Control', 'Connection', 'Content_Length', 'Content_MD5', 'Content_Type',
                 'Cookie', 'DNT', 'Date', 'Expect', 'Forwarded', 'From', 'Front_End_Https', 'If_Match',
                 'If_Modified_Since', 'If_None_Match', 'If_Range', 'If_Unmodified_Since', 'Keep_Alive',
                 'Max_Forwards', 'Origin', 'Permanent', 'Pragma', 'Proxy_Authorization', 'Proxy_Connection',
                 'Range', 'Referer', 'Save_Data', 'TE', 'Upgrade', 'Upgrade_Insecure_Requests', 'User_Agent',
                 'Via', 'Warning', 'X_ATT_DeviceId', 'X_Correlation_ID', 'X_Csrf_Token', 'X_Forwarded_For',
                 'X_Forwarded_Host', 'X_Forwarded_Proto', 'X_Http_Method_Override', 'X_Request_ID',
                 'X_Requested_With', 'X_UIDH', 'X_Wap_Profile']

def get_header(packet):
    headers = {}
    for field in header_fields:
        f = getattr(packet[HTTPRequest], field)
        if f != None and f != 'None':
            headers[field] = f.decode()

    return headers

def sniffing_function(packet):
    if packet.haslayer(HTTPRequest):
        req = Request()

        if packet.haslayer(IP):
            req.origin = packet[IP].src
        else:
            req.origin = 'localhost'

        req.host = urllib.parse.unquote(packet[HTTPRequest].Host.decode())
        req.request = urllib.parse.unquote(packet[HTTPRequest].Path.decode())
        req.method = packet[HTTPRequest].Method.decode()
        req.headers = get_header(packet)
        req.threat_type = 'None'

        if packet.haslayer(Raw):
            req.body = packet[Raw].load.decode()

        # Classify and save the request
        threat_clf.classify_request(req)
        db.save(req)

# Update filter to include the port specified by the user
filter = 'port ' + str(args.port)  # Only capture traffic on the given port
pkgs = sniff(prn=sniffing_function, iface=args.iface, filter=filter, session=TCPSession)

db.close()
