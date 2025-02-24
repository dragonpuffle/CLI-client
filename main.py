import argparse
from sender import send_msg

def parse_args():
    parser = argparse.ArgumentParser(description='CLI for sending msgs')
    parser.add_argument('--sender', help='Sender\'s number')
    parser.add_argument('--recipient', help='Receiver\'s number')
    parser.add_argument('--msg', help='Message')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    response = send_msg(args.sender, args.recipient, args.msg)
    # python main.py --sender 89036666666 --recipient 89995676435 --msg 'hello'