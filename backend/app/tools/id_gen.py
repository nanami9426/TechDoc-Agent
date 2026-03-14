import uuid


def get_id():
    # 无横杠格式
    uid = uuid.uuid4().hex
    return uid
