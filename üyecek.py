from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import os
import random

api_id = 
api_hash = ''
phone = ''



client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('üyü eklenecek grubu seç:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Numara gir: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

mode = int(input("Kullanıcı adına göre eklemek için 1 veya kimliğe göre eklemek için 2 girin: "))
a=0
say=0
for user in users:
    try:
        print ("ekleniyor {}".format(user['id']))
        a=a+1
        if a%30 == 0:
            print("200 sn mola")
            time.sleep(200)
            
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
            say=say+1
            print(say,". kişi eklendi")
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            giz=False
        else:
            sys.exit("Geçersiz Mod Seçildi. Lütfen tekrar deneyin.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("mola")
        
        
        time.sleep(random.randrange(60, 180))
    except PeerFloodError:
        print("Flood hatası")
    except UserPrivacyRestrictedError:
        
        print("Gizlilik ayrı, kullanıcı geçiliyor")
    except:
        traceback.print_exc()
        time.sleep(300)
        print("Unexpected Error")
        continue

