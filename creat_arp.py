# Scapy 라이브러리에서 필요한 모든 기능을 import
from scapy.all import *
# 명령행 인자를 처리하기 위해 sys 모듈 사용
import sys

def send_arp_request(target_ip):
    """
    특정 IP 주소에 대한 ARP 요청을 전송하고, 응답을 받는 함수
    - target_ip: ARP 요청을 보낼 대상의 IP 주소
    """
    
    # ARP 요청을 전송 중임을 사용자에게 알림
    print(f"[*] {target_ip}에 대한 ARP 요청을 전송 중...")
    
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
            print(f"[+] {target_ip}의 MAC 주소: {receive[ARP].hwsrc}")
    else:
        # 응답이 없으면 해당 IP에서 응답이 없다는 메시지를 출력
        print(f"[!] {target_ip}에서 응답이 없습니다.")

if __name__ == "__main__":
    """
    스크립트의 메인 실행 부분
    명령행 인자로 전달된 IP 주소를 사용하여 ARP 요청을 보냄
    """
    
    # sys.argv는 명령행에서 전달된 인자들을 담고 있는 리스트
    # sys.argv[0]은 스크립트의 이름, sys.argv[1]은 첫 번째 인자로 전달된 값 (IP 주소)
    
    # 만약 인자의 개수가 2가 아니라면 (스크립트 이름 + IP 주소가 없으면)
    if len(sys.argv) != 2:
        # 사용자에게 스크립트 사용법을 알려줌
        print(f"사용법: python {sys.argv[0]} <타겟 IP 주소>")
        # 프로그램을 종료 (exit code 1은 오류를 의미)
        sys.exit(1)
    
    # 명령행 인자로 전달된 IP 주소를 target_ip 변수에 저장
    # sys.argv[1]은 사용자가 입력한 타겟 IP 주소
    target_ip = sys.argv[1]
    
    # ARP 요청을 전송하는 함수를 호출
    send_arp_request(target_ip)
