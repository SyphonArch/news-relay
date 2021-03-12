import thecampy
from credentials import user_id, user_pw

soldier = thecampy.Soldier('현재익', 2000_03_14, 2021_03_29)


def send(subject, content):
    try:
        msg = thecampy.Message(subject, content)
        tc = thecampy.client()
        tc.login(user_id, user_pw)

        add_result = tc.add_soldier(soldier)
        get_result = tc.get_soldier(soldier)
        send_result = tc.send_message(soldier, msg)
        return True
    except Exception as p:
        return False
