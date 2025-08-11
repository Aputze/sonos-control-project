import requests
import json
import time
from typing import List, Dict, Optional

class SonosController:
    """Controller for Sonos speakers on the network"""
    
    def __init__(self):
        self.base_url = "http://{ip}:1400/xml/device_description.xml"
        self.control_url = "http://{ip}:1400/MediaRenderer/AVTransport/Control"
        self.rendering_url = "http://{ip}:1400/MediaRenderer/RenderingControl/Control"
        
    def discover_speakers(self) -> List[Dict]:
        """Discover Sonos speakers on the network using SSDP"""
        import socket
        
        speakers = []
        ssdp_request = (
            "M-SEARCH * HTTP/1.1\r\n"
            "HOST: 239.255.255.250:1900\r\n"
            "MAN: \"ssdp:discover\"\r\n"
            "MX: 3\r\n"
            "ST: urn:schemas-upnp-org:device:ZonePlayer:1\r\n"
            "\r\n"
        )
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            sock.sendto(ssdp_request.encode(), ("239.255.255.250", 1900))
            
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    if b"Sonos" in data:
                        # Extract IP address
                        ip = addr[0]
                        # Try to get speaker name
                        name = self._get_speaker_name(ip)
                        speakers.append({"name": name, "ip": ip})
                except socket.timeout:
                    break
                    
        except Exception as e:
            print(f"Error discovering speakers: {e}")
            
        return speakers
    
    def _get_speaker_name(self, ip: str) -> str:
        """Get the name of a Sonos speaker"""
        try:
            response = requests.get(f"http://{ip}:1400/xml/device_description.xml", timeout=5)
            if response.status_code == 200:
                # Simple XML parsing to get device name
                if "<friendlyName>" in response.text:
                    start = response.text.find("<friendlyName>") + 14
                    end = response.text.find("</friendlyName>", start)
                    return response.text[start:end]
        except:
            pass
        return f"Sonos Speaker ({ip})"
    
    def get_speakers(self) -> List[Dict]:
        """Get list of available speakers"""
        return self.discover_speakers()
    
    def play(self, speaker_name: str) -> bool:
        """Play music on the specified speaker"""
        speaker = self._get_speaker_by_name(speaker_name)
        if not speaker:
            return False
            
        soap_body = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <Speed>1</Speed>
                </u:Play>
            </s:Body>
        </s:Envelope>"""
        
        try:
            response = requests.post(
                self.control_url.format(ip=speaker["ip"]),
                data=soap_body,
                headers={"Content-Type": "text/xml; charset=utf-8"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def pause(self, speaker_name: str) -> bool:
        """Pause music on the specified speaker"""
        speaker = self._get_speaker_by_name(speaker_name)
        if not speaker:
            return False
            
        soap_body = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                </u:Pause>
            </s:Body>
        </s:Envelope>"""
        
        try:
            response = requests.post(
                self.control_url.format(ip=speaker["ip"]),
                data=soap_body,
                headers={"Content-Type": "text/xml; charset=utf-8"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def stop(self, speaker_name: str) -> bool:
        """Stop music on the specified speaker"""
        speaker = self._get_speaker_by_name(speaker_name)
        if not speaker:
            return False
            
        soap_body = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:Stop xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                </u:Stop>
            </s:Body>
        </s:Envelope>"""
        
        try:
            response = requests.post(
                self.control_url.format(ip=speaker["ip"]),
                data=soap_body,
                headers={"Content-Type": "text/xml; charset=utf-8"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def set_volume(self, speaker_name: str, volume: int) -> bool:
        """Set volume on the specified speaker (0-100)"""
        speaker = self._get_speaker_by_name(speaker_name)
        if not speaker:
            return False
            
        # Convert to Sonos volume format (0-100)
        sonos_volume = max(0, min(100, volume))
        
        soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
                    <InstanceID>0</InstanceID>
                    <Channel>Master</Channel>
                    <DesiredVolume>{sonos_volume}</DesiredVolume>
                </u:SetVolume>
            </s:Body>
        </s:Envelope>"""
        
        try:
            response = requests.post(
                self.rendering_url.format(ip=speaker["ip"]),
                data=soap_body,
                headers={"Content-Type": "text/xml; charset=utf-8"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_now_playing(self, speaker_name: str) -> Optional[Dict]:
        """Get current track information"""
        speaker = self._get_speaker_by_name(speaker_name)
        if not speaker:
            return None
            
        soap_body = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                </u:GetPositionInfo>
            </s:Body>
        </s:Envelope>"""
        
        try:
            response = requests.post(
                self.control_url.format(ip=speaker["ip"]),
                data=soap_body,
                headers={"Content-Type": "text/xml; charset=utf-8"},
                timeout=5
            )
            
            if response.status_code == 200:
                # Parse XML response to extract track info
                # This is a simplified version - you might want to use proper XML parsing
                text = response.text
                title = self._extract_xml_value(text, "dc:title")
                artist = self._extract_xml_value(text, "dc:creator")
                album = self._extract_xml_value(text, "upnp:album")
                
                return {
                    "title": title or "Unknown",
                    "artist": artist or "Unknown",
                    "album": album or "Unknown"
                }
        except:
            pass
            
        return None
    
    def _extract_xml_value(self, xml_text: str, tag: str) -> str:
        """Extract value from XML tag"""
        try:
            start_tag = f"<{tag}>"
            end_tag = f"</{tag}>"
            start = xml_text.find(start_tag)
            if start != -1:
                start += len(start_tag)
                end = xml_text.find(end_tag, start)
                if end != -1:
                    return xml_text[start:end]
        except:
            pass
        return ""
    
    def _get_speaker_by_name(self, name: str) -> Optional[Dict]:
        """Get speaker by name from discovered speakers"""
        speakers = self.get_speakers()
        for speaker in speakers:
            if speaker["name"] == name:
                return speaker
        return None
