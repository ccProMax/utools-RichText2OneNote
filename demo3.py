# 第三个版本，目前没有任何问题了。
import win32clipboard
from bs4 import BeautifulSoup

try:
    # 获取剪贴板中的text/html格式的源码
    win32clipboard.OpenClipboard()
    clipboard_html = win32clipboard.GetClipboardData(
        win32clipboard.RegisterClipboardFormat("HTML Format"))
    win32clipboard.CloseClipboard()

    # 解析HTML源码，并将源码中的Microsoft YaHei UI全部改为Consolas
    # print(type(clipboard_html))
    soupbak = BeautifulSoup(clipboard_html, 'html.parser')
    soup = str(soupbak)
    soup.replace("Microsoft YaHei UI", "Consolas")
    # soup = BeautifulSoup(bytes(soup), 'html.parser')
    soup = BeautifulSoup(soup, 'html.parser')

    # 解析HTML源码并删除背景色
    for tag in soup.find_all(True):
        tag.attrs = {key: val for key, val in tag.attrs.items(
        ) if key != 'style' or 'background' not in val}

    # 将修改后的HTML源码重新写入剪贴板中
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat(
        "HTML Format"), str(soup).encode('utf-8'))
    win32clipboard.CloseClipboard()

except Exception as err:
    print('错误', err)
