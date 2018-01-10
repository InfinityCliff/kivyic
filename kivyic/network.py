import socket
from kivyic import DEBUG_INTERNET


def internet_online(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    if DEBUG_INTERNET:  # If debugging internet issues, when True
        return False    # will return False to fake internet not being available
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == '__main__':
    print(internet_online())