import uuid
import datetime
from db import DbManager, User, Audio


def create_user(name: str) -> dict:
    data_user = {
        'name': name,
        'id': uuid.uuid4(),
        'token': uuid.uuid4(),
        'created_at': datetime.datetime.now()
    }

    DbManager().create_record(data_user, User)

    return data_user


def create_mp3(file: bytes, user_id: str, token: str) -> dict:
    data_mp3 = {
        'id': uuid.uuid4(),
        'user_id': user_id,
        'mp3': file,
        'created_at': datetime.datetime.now()
    }

    if DbManager().check_user_token(user_id, token):
        DbManager().create_record(data_mp3, Audio)
        url = f"http://localhost:8000/record?id={data_mp3['id']}&user={data_mp3['user_id']}"
    else:
        url = None

    return url


def get_mp3(mp3_id: str, user_id: str):
    path_to_mp3 = DbManager().get_mp3(mp3_id, user_id)
    return path_to_mp3


if __name__ == '__main__':
    print(create_user("Ivan Sidorov"))
