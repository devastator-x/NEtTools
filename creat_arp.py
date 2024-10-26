# Scapy 라이브러리에서 필요한 모든 기능을 import
from scapy.all import *
# 명령행 인자를 처리하기 위해 sys 모듈과 argparse 모듈 사용
import sys
import time
import argparse

def send_arp_request(target_ip, count, continuous):
    """
    특정 IP 주소에 대한 ARP 요청을 여러 번 또는 지속적으로 전송하고, 응답을 받는 함수
    - target_ip: ARP 요청을 보낼 대상의 IP 주소
    - count: 전송할 ARP 패킷의 수 (continuous가 True일 때는 무시됨)
    - continuous: True일 경우 사용자가 멈출 때까지 지속적으로 패킷을 전송
    """
    
    if continuous:
        print(f"[*] Continuously sending ARP requests to {target_ip}...")
    else:
        print(f"[*] Sending {count} ARP requests to {target_ip}...")
    
    try:
        i = 0
        while continuous or i < count:
            # ARP 요청 패킷을 생성
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
            
            # srp() 함수는 Layer 2 (Ethernet) 계층에서 패킷을 전송하고 응답을 대기하는 함수
            answered, unanswered = srp(arp_request, timeout=2, verbose=False)
            
            # 응답이 있는 경우 응답한 패킷들에 대한 MAC 주소를 출력
            if answered:
                for send, receive in answered:
                    print(f"[{i+1}] [+] MAC address for {target_ip}: {receive[ARP].hwsrc}")
            else:
                print(f"[{i+1}] [!] No response from {target_ip}")
            
            i += 1
            # 각 ARP 요청 후 1초 대기
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n[!] ARP request stopped by user.")

if __name__ == "__main__":
    """
    스크립트의 메인 실행 부분
    명령행 인자로 전달된 IP 주소와 패킷 수, 또는 지속 전송 옵션을 사용하여 ARP 요청을 보냄
    """
    
    # argparse를 사용하여 명령행 인자 처리
    parser = argparse.ArgumentParser(description="Script to send ARP requests")
    # target_ip 인자는 ARP 요청을 보낼 타겟 IP 주소를 지정
    parser.add_argument("target_ip", help="Target IP address to send ARP request")
    # -c 또는 --count 플래그는 ARP 요청을 보낼 횟수를 지정하며, 기본값은 1회로 설정
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of ARP requests to send (default: 1)")
    # -t 플래그는 사용자가 중지할 때까지 ARP 요청을 지속적으로 보냄
    parser.add_argument("-t", "--continuous", action="store_true", help="Send ARP requests continuously until stopped")
    args = parser.parse_args()
    
    # ARP 요청을 전송하는 함수를 호출
    send_arp_request(args.target_ip, args.count, args.continuous)
