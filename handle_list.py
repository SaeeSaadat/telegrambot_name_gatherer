import sqlite3
from typing import List


def get_members(chat_instance: str, inline_message_id: str) -> List[str]:
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('select members from lists where chat_instance = ? and inline_message_id = ?',
                       (chat_instance, inline_message_id))
        res = cursor.fetchone()
        if res:
            members = res[0].split(' ')
        else:
            members = []

        return members


def update_members(chat_instance: str, inline_message_id: str, new_members: List[str]) -> None:
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        members = ' '.join(new_members)
        cursor.execute('update lists set members = ? where chat_instance = ? and inline_message_id = ?',
                       (members, chat_instance, inline_message_id))
        conn.commit()
