import asyncio
import aiosmtplib
import aiosqlite
from email.message import EmailMessage


async def get_db():
    conn = await aiosqlite.connect('contacts.db')
    cur = await conn.execute("SELECT * FROM contacts")
    rows = await cur.fetchall()
    res = []
    for i in rows:
        res.append({"name": i[1], "email": i[3]})
    await conn.close()
    return res

async def send_email(name, email):
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = email
    message["Subject"] = f"Уважаемый {name}! \nСпасибо, что пользуетесь нашим сервисом объявлений!"
    message.set_content()
    await aiosmtplib.send(message, hostname="127.0.0.1", port=1025)

async def main():
    ready_messages = []
    get_users = get_db()
    for user in get_users:
        data_user = send_email(
            user["name"],
            user["email"],
        )
        ready_messages.append(data_user)
    send = await asyncio.gather(*ready_messages)
    return send

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())

