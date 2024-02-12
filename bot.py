import telebot
from telebot import types
import subprocess
import os

os.system("clear")

ascii_art = """
______     ______ 
| ___ \    |  ___|
| |_/ /__ _| |_   
|    // _` |  _|  
| |\ \ (_| | |    
\_| \_\__,_\_|    
This Telegram bot its features 
• Upload file
• Delete file 
• View files 
The important and distinctive thing is the terminal 
telegram @x10xxx
"""

print(ascii_art)

TOKEN = input("enter token: ")
bot = telebot.TeleBot(TOKEN)
print("your bot run")

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.reply_to(message, 'hi welcome im raf @x10xxx')
    show_inline_keyboard(chat_id)

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    chat_id = message.chat.id
    command = message.text.strip()
    result = execute_command(command)
    if len(result.split('\n')) > 40:
        send_as_file(chat_id, result)
    else:
        bot.send_message(chat_id, result)

def send_as_file(chat_id, text):
    with open('output.txt', 'w') as f:
        f.write(text)
    with open('output.txt', 'rb') as f:
        bot.send_document(chat_id, f)

def show_inline_keyboard(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    upload_button = types.InlineKeyboardButton("upload", callback_data='upload')
    delete_button = types.InlineKeyboardButton("delete", callback_data='delete')
    show_files_button = types.InlineKeyboardButton("show files", callback_data='show_files')
    download_button = types.InlineKeyboardButton("download file", callback_data='download_file')
    terminal_button = types.InlineKeyboardButton("terminal", callback_data='terminal')
    copy_button = types.InlineKeyboardButton("copy text", callback_data='copy_text')
    markup.add(upload_button, delete_button, show_files_button, download_button, terminal_button, copy_button)
    bot.send_message(chat_id, "hi welcome im raf @x10xxx", reply_markup=markup)

def execute_command(command):
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            return output
        else:
            error_message = result.stderr.strip()
            return "Error executing command:\n" + error_message
    except Exception as e:
        return f'Error: {e}'

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    chat_id = call.message.chat.id
    if call.data == 'upload':
        bot.send_message(chat_id, 'Send file ')
        bot.register_next_step_handler(call.message, handle_file_upload)
    elif call.data == 'delete':
        bot.send_message(chat_id, 'Send file name to delete: ')
        bot.register_next_step_handler(call.message, handle_file_deletion)
    elif call.data == 'show_files':
        show_files_list(chat_id)
    elif call.data == 'download_file':
        bot.send_message(chat_id, 'Send the name of the file you want to download:')
        bot.register_next_step_handler(call.message, handle_download_file_request)
    elif call.data == 'terminal':
        send_terminal_commands_instructions(chat_id)
    elif call.data == 'copy_text':
        bot.send_message(chat_id, 'This text can be copied.')

def send_terminal_commands_instructions(chat_id):
    markdown_text = """
Send commands you want to execute in the terminal:

- `pwd`: Display current directory path.
- `ls`: File list
- `cd directory_name`: Change to another directory.
- `touch file_name`: Create a new file.
- `mkdir directory_name`: Create new directory.
- `cat file_name`: Display contents of file.
- `rm file_name`: Delete file.
- `uname`: system information
- `history`: Display list previously commands.
- `rm -rf directory_name`: Delete a directory (and its contents).
- `mv source_file_path target_file_path`: Move file from place to another.
- `cp source_file_path target_file_path`: Copy file from place to another.
- `zip` and `unzip`: Compress and decompress ZIP archive files.
Send commands you want to execute in the terminal:
"""
    bot.send_message(chat_id, markdown_text, parse_mode="markdown")

def handle_file_upload(message):
    chat_id = message.chat.id
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(chat_id, f'uploaded successfully : {file_name}')
    else:
        bot.send_message(chat_id, 'The file you sent is invalid. Please send a file.')

def handle_file_deletion(message):
    chat_id = message.chat.id
    file_name = message.text.strip()
    if os.path.exists(file_name):
        os.remove(file_name)
        bot.send_message(chat_id, f'deleted successfully : {file_name}')
    else:
        bot.send_message(chat_id, f'File not found. ')

def show_files_list(chat_id):
    files_list = "\n".join(os.listdir())
    bot.send_message(chat_id, "Files in directory:\n" + files_list)

def handle_download_file_request(message):
    chat_id = message.chat.id
    file_name = message.text.strip()
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            bot.send_document(chat_id, f, caption=f'Download {file_name}')
    else:
        bot.send_message(chat_id, f'File {file_name} not found.')

bot.polling()
