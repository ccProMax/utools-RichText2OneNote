import pyperclip
import win32clipboard
from bs4 import BeautifulSoup

# 获取剪贴板中的text/html格式的源码
win32clipboard.OpenClipboard()
clipboard_html = win32clipboard.GetClipboardData(win32clipboard.RegisterClipboardFormat("HTML Format"))
win32clipboard.CloseClipboard()

# 解析HTML源码
soup = BeautifulSoup(clipboard_html, 'html.parser')

for tag in soup.find_all():
    if tag.has_attr('style'):
        style = tag['style']
        if 'background-color' in style:
            new_style = '; '.join([s.strip() for s in style.split(';') if 'background-color' not in s])
            tag['style'] = new_style
        else:
            continue
# 将修改后的HTML源码重新写入剪贴板中
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat("HTML Format"), str(soup).encode('utf-8'))
win32clipboard.CloseClipboard()
