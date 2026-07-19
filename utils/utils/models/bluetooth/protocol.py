import json
from models.message import ChatMessage

class Protocol:
    DELIMITER = b'\n'

    @staticmethod
    def encode(msg: ChatMessage) -> bytes:
        data = json.dumps(msg.to_dict())
        return data.encode('utf-8') + Protocol.DELIMITER

    @staticmethod
    def decode(data_buffer: bytearray):
        messages = []
        while Protocol.DELIMITER in data_buffer:
            packet, data_buffer = data_buffer.split(Protocol.DELIMITER, 1)
            if packet:
                try:
                    msg_dict = json.loads(packet.decode('utf-8'))
                    messages.append(msg_dict)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
        return messages, data_buffer
