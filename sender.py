import thecampy
from credentials import user_id, user_pw

soldier = thecampy.Soldier('현재익', 2000_03_14, 2021_03_29, '육군훈련소')


def send(subject, content):
    content += '\n[FINISH]'
    msg_num = 0
    char_count = 0
    enter_count = 0
    buffer = []
    for i, char in enumerate(content):
        buffer.append(char)
        char_count += 1
        if char == '\n':
            enter_count += 1

        if char_count > 1495 or enter_count > 22 or i == len(content) - 1:
            _send(subject + f" - {msg_num}", ''.join(buffer))

            char_count = 0
            enter_count = 0
            buffer = []

            msg_num += 1


def _send(subject, content):
    try:
        msg = thecampy.Message(subject, content)
        tc = thecampy.client()
        tc.login(user_id, user_pw)

        get_result = tc.get_soldier(soldier)
        send_result = tc.send_message(soldier, msg)
        return True
    except Exception as p:
        return False
