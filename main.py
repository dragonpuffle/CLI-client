import argparse
from sender import send_msg
from logger import LOGGER


def parse_args():
    parser = argparse.ArgumentParser(description='CLI for sending msgs')
    parser.add_argument('--sender', help='Sender\'s number')
    parser.add_argument('--recipient', help='Receiver\'s number')
    parser.add_argument('--msg', help='Message')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    LOGGER.info(f'Sender {args.sender} sent to recipient {args.recipient} msg {args.msg}')
    response = send_msg(args.sender, args.recipient, args.msg)
    LOGGER.info(f'Client got a response from server: {response}')

    # python main.py --sender 89036666666 --recipient 89995676435 --msg 'hello'