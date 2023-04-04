# 最终版本，目前没有遇到问题
import win32clipboard
from bs4 import BeautifulSoup


# 获取剪贴板中的text/html格式的源码
def getsoup():
    win32clipboard.OpenClipboard()
    clipboard_html = win32clipboard.GetClipboardData(
        win32clipboard.RegisterClipboardFormat("HTML Format"))
    win32clipboard.CloseClipboard()
    soup = BeautifulSoup(clipboard_html, 'html.parser')
    return soup


# 删除背景色
def delbackground(soup):
    for tag in soup.find_all(True):
        tag.attrs = {key: val for key, val in tag.attrs.items(
        ) if key != 'style' or 'background' not in val}
    return soup


# 将soup中第一个div里的字体大小改为14px。顺便将字体设置为'Consolas'
def fontSize(soup):
    div_tag = soup.find('div')
    # 获取style属性
    style_str = div_tag.get('style')
    # 将style属性解析为字典
    style_dict = {}
    if style_str:
        for style in style_str.split(';'):
            if style:
                key, value = style.split(':')
                style_dict[key.strip()] = value.strip()
    # 更新字典中的font-size属性
    style_dict['font-size'] = '14px'
    style_dict['font-family'] = 'Consolas'
    # 将字典转换为字符串
    new_style_str = '; '.join(
        [f'{key}: {value}' for key, value in style_dict.items()])
    # 将新的style属性设置回div标签
    div_tag['style'] = new_style_str
    return soup

# 去除所有span中的字体设置
def delspanfont(soup):
    # 找到所有的span标签
    span_tags = soup.find_all('span')
    # 遍历所有的span标签
    for span_tag in span_tags:
        # 获取style属性
        style_str = span_tag.get('style')
        # 将style属性解析为字典
        style_dict = {}
        if style_str:
            for style in style_str.split(';'):
                if style:
                    key, value = style.split(':')
                    style_dict[key.strip()] = value.strip()
            # 移除font-family属性
            if 'font-family' in style_dict:
                del style_dict['font-family']
            # 将字典转换为字符串
            new_style_str = '; '.join(
                [f'{key}: {value}' for key, value in style_dict.items()])
            # 将新的style属性设置回span标签
            span_tag['style'] = new_style_str
    return soup

# 将修改后的HTML源码重新写入剪贴板中
def clipboard(soup):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat(
        "HTML Format"), str(soup).encode('utf-8'))
    win32clipboard.CloseClipboard()


if __name__ == '__main__':
    try:
        soup = getsoup()
        soup = delbackground(soup)
        soup = fontSize(soup)
        soup = delspanfont(soup)
        clipboard(soup)
    except Exception as err:
        print('Error', err)
    else:
        print("OK")
