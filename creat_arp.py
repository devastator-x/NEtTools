# Scapy 라이브러리에서 필요한 모든 기능을 import
from scapy.all import *
# 명령행 인자를 처리하기 위해 sys 모듈과 argparse 모듈 사용
import sys
import time
import argparse

def send_arp_request(target_ip, count):
    """
    특정 IP 주소에 대한 ARP 요청을 여러 번 전송하고, 응답을 받는 함수
    - target_ip: ARP 요청을 보낼 대상의 IP 주소
    - count: 전송할 ARP 패킷의 수
    """
    
    # ARP 요청을 전송 중임을 사용자에게 알림
    print(f"[*] Sending {count} ARP requests to {target_ip}...")
    
    # 지정한 횟수만큼 ARP 요청을 전송
    for i in range(count):
        # ARP 요청 패킷을 생성
        # Ether(dst="ff:ff:ff:ff:ff:ff")는 이더넷 브로드캐스트 주소로 설정
        # ARP(pdst=target_ip)는 대상 IP 주소로 ARP 요청 패킷을 생성
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
        
        # srp() 함수는 Layer 2 (Ethernet) 계층에서 패킷을 전송하고 응답을 대기하는 함수
        # arp_request: 생성한 ARP 요청 패킷
        # timeout=2: 응답을 기다리는 시간(초)
        # verbose=False: 불필요한 정보를 출력하지 않도록 설정
        answered, unanswered = srp(arp_request, timeout=2, verbose=False)
        
        # 응답이 있는 경우 응답한 패킷들에 대한 MAC 주소를 출력
        if answered:
            # answered는 (발신 패킷, 수신 패킷) 쌍의 리스트를 반환
            for send, receive in answered:
                # 수신된 패킷의 ARP 레이어에서 MAC 주소(hwsrc)를 추출하여 출력
                print(f"[{i+1}/{count}] [+] MAC address for {target_ip}: {receive[ARP].hwsrc}")
        else:
            # 응답이 없으면 해당 IP에서 응답이 없다는 메시지를 출력
            print(f"[{i+1}/{count}] [!] No response from {target_ip}")
        
        # 각 ARP 요청 후 1초 대기
        time.sleep(1)

if __name__ == "__main__":
    """
    스크립트의 메인 실행 부분
    명령행 인자로 전달된 IP 주소와 패킷 수를 사용하여 ARP 요청을 보냄
    """
    
    # argparse를 사용하여 명령행 인자 처리
    parser = argparse.ArgumentParser(description="ARP 요청을 보내는 스크립트")
    # target_ip 인자는 ARP 요청을 보낼 타겟 IP 주소를 지정
    parser.add_argument("target_ip", help="ARP 요청을 보낼 타겟 IP 주소")
    # -c 또는 --count 플래그는 ARP 요청을 보낼 횟수를 지정하며, 기본값은 1회로 설정
    parser.add_argument("-c", "--count", type=int, default=1, help="ARP 요청을 보낼 횟수 (기본값: 1회)")
    args = parser.parse_args()
    
    # ARP 요청을 전송하는 함수를 호출
    send_arp_request(args.target_ip, args.count)
