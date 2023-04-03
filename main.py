import os
import threading
import subprocess
import time

import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton

import mdisk
import extras
import mediainfo
import split
from split import TG_SPLIT_SIZE


# app
bot_token = os.environ.get("TOKEN", "6102213171:AAFqrMySBjy18lbZfXbZnLJapYEbQbFIhZw") 
api_hash = os.environ.get("HASH", "926c0e413170fdbcd92beb1b271ebed0") 
api_id = os.environ.get("ID", "26852014")
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# preiumum
from split import ss, temp_channel, isPremmium
if isPremmium: acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)

# optionals
auth = os.environ.get("AUTH", "1961852781")
ban = os.environ.get("BAN", "")
from mdisk import iswin

# start command
@app.on_message(filters.command(["start"]))
def echo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**', reply_to_message_id=message.id,reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("☆    ᴏᴡɴᴇʀ    ☆", url="https://t.me/Mxxn_Knight")]]))
        return

    app.send_message(message.chat.id, '**ʜɪ ,ɪ ᴀᴍ ᴍᴅɪsᴋ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ, ʏᴏᴜ ᴄᴀɴ ᴡᴀᴛᴄʜ ᴠɪᴅᴇᴏs ᴡɪᴛʜᴏᴜᴛ ᴍx ᴘʟᴀʏᴇʀ.\n sᴇɴᴛ ᴍᴇ ᴛʜᴇ ʟɪɴᴋ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ...**',reply_to_message_id=message.id,
    reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("☆    ᴏᴡɴᴇʀ    ☆ ", url="https://t.me/Mxxn_Knight")]]))

# help command
@app.on_message(filters.command(["help"]))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return
    
    helpmessage = """**/sᴛᴀʀᴛ   - ᴄʜᴇᴄᴋ ᴀʟɪᴠᴇ**
**/ʜᴇʟᴘ   - ᴛʜɪs ᴍᴇssᴀɢᴇ**
**/ᴍᴅɪsᴋ ᴍᴅɪsᴋʟɪɴᴋ - ᴜsᴀɢᴇ**
**/ᴛʜᴜᴍʙ - ʀᴇᴘʟʏ ᴛᴏ ᴀ ɪᴍᴀɢᴇ ᴅᴏᴄᴜᴍᴇɴᴛ ᴏғ sɪᴢᴇ ʟᴇss ᴛʜᴀɴ 200ᴋʙ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴛʜᴜᴍʙɴᴀɪʟ ( ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇɴᴅ ɪᴍᴀɢᴇ ᴀs ᴀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴛʜᴜᴍʙɴᴀɪʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ )**
**/ʀᴇᴍᴏᴠᴇ - ʀᴇᴍᴏᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ**
**/sʜᴏᴡ   - sʜᴏᴡ ᴛʜᴜᴍʙɴᴀɪʟ**
**/ᴄʜᴀɴɢᴇ - ᴄʜᴀɴɢᴇ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ (ᴅᴇғᴀᴜʟᴛ ᴍᴏᴅ ɪs ᴅᴏᴄᴜᴍᴇɴᴛ)**"""
    app.send_message(message.chat.id, helpmessage, reply_to_message_id=message.id)


# check for user access
def checkuser(message):
    if auth != "" or ban != "":
        valid = 1
        if auth != "":
            authusers = auth.split(",")
            if str(message.from_user.id) not in authusers:
                valid = 0
        if ban != "":
            bannedusers = ban.split(",")
            if str(message.from_user.id) in bannedusers:
                valid = 0
        return valid        
    else:
        return 1


# download status
def status(folder,message,fsize):
    fsize = fsize / pow(2,20)
    length = len(folder)
    # wait for the folder to create
    while True:
        if os.path.exists(folder + "/vid.mp4.part-Frag0") or os.path.exists(folder + "/vid.mp4.part"):
            break
    
    time.sleep(3)
    while os.path.exists(folder + "/" ):
        if iswin == "0":
            result = subprocess.run(["du", "-hs", f"{folder}/"], capture_output=True, text=True)
            size = result.stdout[:-(length+2)]
        else:
            os.system(f"dir /a/s {folder} > tempS-{message.id}.txt")
            size = str(int(open(f"tempS-{message.id}.txt","r").readlines()[-2].split()[2].replace(",","")) // 1000000) + "ᴍʙ "

        try:
            app.edit_message_text(message.chat.id, message.id, f"__ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ__ : **{size} **__ᴏғ__**  {fsize:.1f}M**")
            time.sleep(10)
        except:
            time.sleep(5)

    if iswin != "0": os.remove(f"tempS-{message.id}.txt")


# upload status
def upstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as upread:
            txt = upread.read()
        try:
            app.edit_message_text(message.chat.id, message.id, f"__ᴜᴘʟᴏᴀᴅᴇᴅ__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# progress writter
def progress(current, total, message):
    with open(f'{message.id}upstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# download and upload
def down(message,link):

    # checking link and download with progress thread
    msg = app.send_message(message.chat.id, '__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ__', reply_to_message_id=message.id)
    size = mdisk.getsize(link)
    if size == 0:
        app.edit_message_text(message.chat.id, msg.id,"__**ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ**__")
        return
    sta = threading.Thread(target=lambda:status(str(message.id),msg,size),daemon=True)
    sta.start()

    # checking link and download and merge
    file,check,filename = mdisk.mdow(link,message)
    if file == None:
        app.edit_message_text(message.chat.id, msg.id,"__**ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ**__")
        return

    # checking if its a link returned
    if check == -1:
        app.edit_message_text(message.chat.id, msg.id,f"__**ᴄᴀɴ'ᴛ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ ʙᴜᴛ ʜᴇʀᴇ ɪs ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ: {file}**__")
        os.rmdir(str(message.id))
        return

    # checking size
    size = split.get_path_size(file)
    if(size > TG_SPLIT_SIZE):
        app.edit_message_text(message.chat.id, msg.id, "__sᴘʟɪᴛᴛɪɴɢ__")
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        os.remove(file) 
    else:
        flist = [file]
    app.edit_message_text(message.chat.id, msg.id, "__ᴜᴘʟᴏᴀᴅɪɴɢ__")
    i = 1

    # checking thumbline
    if not os.path.exists(f'{message.from_user.id}-thumb.jpg'):
        thumbfile = None
    else:
        thumbfile = f'{message.from_user.id}-thumb.jpg'

    # upload thread
    upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',msg),daemon=True)
    upsta.start()
    info = extras.getdata(str(message.from_user.id))

    # uploading
    for ele in flist:

        # checking file existence
        if not os.path.exists(ele):
            app.send_message(message.chat.id,"**ᴇʀʀᴏʀ ɪɴ ᴍᴇʀɢɪɴɢ ғɪʟᴇ**",reply_to_message_id=message.id)
            return
            
        # check if it's multi part
        if len(flist) == 1:
            partt = ""
        else:
            partt = f"__**part {i}**__\n"
            i = i + 1

        # actuall upload
        if info == "V":
            thumb,duration,width,height = mediainfo.allinfo(ele,thumbfile)
            if not isPremmium : app.send_video(message.chat.id, video=ele, caption=f"{partt}**{filename}**", thumb=thumb, duration=duration, height=height, width=width, reply_to_message_id=message.id, progress=progress, progress_args=[message])
            else:
                with acc: tmsg = acc.send_video(temp_channel, video=ele, caption=f"{partt}**{filename}**", thumb=thumb, duration=duration, height=height, width=width, progress=progress, progress_args=[message])
                app.copy_message(message.chat.id, temp_channel, tmsg.id, reply_to_message_id=message.id)
            if "-thumb.jpg" not in thumb: os.remove(thumb)
        else:
            if not isPremmium : app.send_document(message.chat.id, document=ele, caption=f"{partt}**{filename}**", thumb=thumbfile, force_document=True, reply_to_message_id=message.id, progress=progress, progress_args=[message])
            else:
                with acc: tmsg = acc.send_document(temp_channel, document=ele, thumb=thumbfile, caption=f"{partt}**{filename}**", force_document=True, progress=progress, progress_args=[message])
                app.copy_message(message.chat.id, temp_channel, tmsg.id, reply_to_message_id=message.id)
       
        # deleting uploaded file
        os.remove(ele)
        
    # checking if restriction is removed    
    if check == 0:
        app.send_message(message.chat.id,"__ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴛʜᴇ **ʀᴇsᴛʀɪᴄᴛɪᴏɴ**, ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴜsᴇ**ᴍx ᴘʟᴀʏᴇʀ** ᴛᴏ ᴘʟᴀʏ ᴛʜɪs**ᴠɪᴅᴇᴏ**\n\nᴛʜɪs ʜᴀᴘᴘᴇɴs ʙᴇᴄᴀᴜsᴇ ᴇɪᴛʜᴇʀ ᴛʜᴇ **ғɪʟᴇ** ʟᴇɴɢᴛʜ ɪs**ᴛᴏᴏ sᴍᴀʟʟ** ᴏʀ **ᴠɪᴅᴇᴏ** ᴅᴏᴇsɴ'ᴛ ʜᴀᴠᴇ sᴇᴘᴀʀᴀᴛᴇ**ᴀᴜᴅɪᴏ ʟᴀʏᴇʀ**__",reply_to_message_id=message.id)
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    app.delete_messages(message.chat.id,message_ids=[msg.id])


# mdisk command
@app.on_message(filters.command(["mdisk"]))
def mdiskdown(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return

    try:
        link = message.text.split("mdisk ")[1]
        if "https://mdisk.me/" in link:
            d = threading.Thread(target=lambda:down(message,link),daemon=True)
            d.start()
            return 
    except:
        pass

    app.send_message(message.chat.id, '**sᴇɴᴅ ᴏɴʟʏ __ᴍᴅɪsᴋ ʟɪɴᴋ__ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ ғᴏʟʟᴏᴡᴇᴅ ʙʏ ᴛʜᴇ ʟɪɴᴋ**',reply_to_message_id=message.id)


# thumb command
@app.on_message(filters.command(["thumb"]))
def thumb(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return

    try:
        if int(message.reply_to_message.document.file_size) > 200000:
            app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ sɪᴢᴇ ɪs ᴀʟʟᴏᴡᴇᴅ ɪs < 200 ᴋʙ**',reply_to_message_id=message.id)
            return

        msg = app.get_messages(message.chat.id, int(message.reply_to_message.id))
        file = app.download_media(msg)
        os.rename(file,f'{message.from_user.id}-thumb.jpg')
        app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ ɪs sᴇᴛ**',reply_to_message_id=message.id)

    except:
        app.send_message(message.chat.id, '**ʀᴇᴘʟʏ __/ᴛʜᴜᴍɴ__ ᴛᴏ ᴀ ɪᴍᴀɢᴇ ᴅᴏᴄᴜᴍᴇɴᴛ ᴏғ sɪᴢᴇ ʟᴇss ᴛʜᴀɴ 200ᴋʙ**',reply_to_message_id=message.id)


# show thumb command
@app.on_message(filters.command(["show"]))
def showthumb(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return
    
    if os.path.exists(f'{message.from_user.id}-thumb.jpg'):
        app.send_photo(message.chat.id,photo=f'{message.from_user.id}-thumb.jpg',reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ ɪs ɴᴏᴛ sᴇᴛ**',reply_to_message_id=message.id)


# remove thumbline command
@app.on_message(filters.command(["remove"]))
def removethumb(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return
    
    
    if os.path.exists(f'{message.from_user.id}-thumb.jpg'):
        os.remove(f'{message.from_user.id}-thumb.jpg')
        app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ ɪs ʀᴇᴍᴏᴠᴇᴅ**',reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ ɪs ɴᴏᴛ sᴇᴛ**',reply_to_message_id=message.id)


# thumbline
@app.on_message(filters.photo)
def ptumb(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return
    
    file = app.download_media(message)
    os.rename(file,f'{message.from_user.id}-thumb.jpg')
    app.send_message(message.chat.id, '**ᴛʜᴜᴍʙɴᴀɪʟ ɪs sᴇᴛ**',reply_to_message_id=message.id)
    

# change mode
@app.on_message(filters.command(["change"]))
def change(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return
    
    info = extras.getdata(str(message.from_user.id))
    extras.swap(str(message.from_user.id))
    if info == "V":
        app.send_message(message.chat.id, '__ᴍᴏᴅᴇ ᴄʜᴀɴɢᴇᴅ ғʀᴏᴍ **ᴠɪᴅᴇᴏ** ғᴏʀᴍᴀᴛ ᴛᴏ**ᴅᴏᴄᴜᴍᴇɴᴛ** ғᴏʀᴍᴀᴛ__',reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, '__ᴍᴏᴅᴇ ᴄʜᴀɴɢᴇᴅ ғʀᴏᴍ **ᴅᴏᴄᴜᴍᴇɴᴛ** ғᴏʀᴍᴀᴛ ᴛᴏ **ᴠɪᴅᴇᴏ** ғᴏʀᴍᴀᴛ__',reply_to_message_id=message.id)

        
# multiple links handler
def multilinks(message,links):
    for link in links:
        d = threading.Thread(target=lambda:down(message,link),daemon=True)
        d.start()
        d.join()


# mdisk link in text
@app.on_message(filters.text)
def mdisktext(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    if isPremmium and message.chat.id == temp_channel: return

    if not checkuser(message):
        app.send_message(message.chat.id, '**ʏᴏᴜ ᴀʀᴇ ᴇɪᴛʜᴇʀ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴏʀ ʙᴀɴɴᴇᴅ**',reply_to_message_id=message.id)
        return

    if message.text[0] == "/":
        app.send_message(message.chat.id, '**sᴇᴇ  __/ʜᴇʟᴘ__**',reply_to_message_id=message.id)
        return

    if "https://mdisk.me/" in message.text:
        links = message.text.split("\n")
        if len(links) == 1:
            d = threading.Thread(target=lambda:down(message,links[0]),daemon=True)
            d.start()
        else:
            d = threading.Thread(target=lambda:multilinks(message,links),daemon=True)
            d.start()   
    else:
        app.send_message(message.chat.id, '**sᴇɴᴅ ᴏɴʟʏ __ᴍᴅɪsᴋ ʟɪɴᴋ__**',reply_to_message_id=message.id)


app.run()

