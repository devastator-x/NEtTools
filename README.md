
# arping

이 프로젝트는 지정된 IP 주소에 ARP (Address Resolution Protocol) 요청을 보내는 Python 스크립트입니다. Scapy 라이브러리를 사용하여 요청을 전송하고 대상의 MAC 주소를 확인합니다. 스크립트는 요청 횟수를 지정하거나 사용자가 중지할 때까지 지속적으로 요청을 보내는 옵션을 제공합니다.

## 요구 사항

- Python 3
- Scapy 라이브러리
    - 설치 명령어: `pip install scapy`

## 사용법

스크립트는 타겟 IP 주소를 인자로 받고, 요청 횟수 지정 또는 지속적인 요청 옵션을 사용할 수 있습니다.

### 기본 명령어

```bash
python arping.py <타겟 IP 주소>
```

- `<타겟 IP 주소>`: 대상 장치의 IP 주소.

### 옵션

- **`-c`, `--count`**: 보낼 ARP 요청의 횟수를 지정 (기본값은 1회).
- **`-t`, `--continuous`**: 사용자가 중지할 때까지 ARP 요청을 지속적으로 전송 (`Ctrl+C`로 중지 가능).

### 사용 예시

1. 타겟 IP에 대해 단일 ARP 요청을 보냅니다:
    ```bash
    python arping.py 192.168.1.1
    ```

2. 다수의 ARP 요청을 보냅니다 (예: 5회 요청):
    ```bash
    python arping.py 192.168.1.1 -c 5
    ```

3. 사용자가 중지할 때까지 지속적으로 ARP 요청을 보냅니다:
    ```bash
    python arping.py 192.168.1.1 -t
    ```

## 출력 예시

스크립트는 대상 장치가 ARP 요청에 응답할 경우 해당 MAC 주소를 출력합니다. 응답이 없으면, 응답이 없다는 메시지를 출력합니다.

예시 출력:
```plaintext
[*] Sending 5 ARP requests to 192.168.1.1...
[1/5] [+] MAC address for 192.168.1.1: aa:bb:cc:dd:ee:ff
[2/5] [+] MAC address for 192.168.1.1: aa:bb:cc:dd:ee:ff
...
```

지속 모드 출력 예시:
```plaintext
[*] Continuously sending ARP requests to 192.168.1.1...
[1] [+] MAC address for 192.168.1.1: aa:bb:cc:dd:ee:ff
...
```

## 주의 사항

- **네트워크 권한**: 환경에 따라 ARP 요청을 보내기 위해 관리자 권한이 필요할 수 있습니다.
- **지속 모드 중단**: `-t` 플래그 사용 시 `Ctrl+C`로 스크립트를 중단할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.
