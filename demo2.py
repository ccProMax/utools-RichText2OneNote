# 第二个版本，能够去除黑色背景，但是字体还是有问题
import win32clipboard
from bs4 import BeautifulSoup

# 获取剪贴板中的text/html格式的源码
win32clipboard.OpenClipboard()
clipboard_html = win32clipboard.GetClipboardData(win32clipboard.RegisterClipboardFormat("HTML Format"))
win32clipboard.CloseClipboard()


# 解析HTML源码
soup = BeautifulSoup(clipboard_html, 'html.parser')


# 解析HTML源码并删除背景色
for tag in soup.find_all(True):
    tag.attrs = {key:val for key,val in tag.attrs.items() if key != 'style' or 'background' not in val}


# 将修改后的HTML源码重新写入剪贴板中
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat("HTML Format"), str(soup).encode('utf-8'))
win32clipboard.CloseClipboard()
