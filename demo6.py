#主要针对公司里的idea。 
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
    div_tag = soup.find('pre')   # find是找第一个
    if div_tag:   # 如果找到
        style_str = "font-family:'Consolas';font-size:9.0pt;"
        div_tag['style'] = style_str
        return soup
    else:  # 否则直接返回。
        return soup



# 去除所有span中的字体设置
def delspanfont(soup):
    # 找到所有的span标签
    span_tags = soup.find_all('span')
    # 遍历所有的span标签
    for span_tag in span_tags:
        # 获取style属性
        style_str = span_tag.get('style')
        if not style_str:  # 如果没有就直接返回了。
            return soup
        # 将style属性解析为字典 style_dict
        style_dict = {}
        for style in style_str.split(';'):  # 通过;分割属性
            if style:  # 如果有，处理得到字典。
                key, value = style.split(':')
                style_dict[key.strip()] = value.strip()
        # 如果字典中有font-family这个key，就删掉。       
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
        soup = getsoup()                     # 得到soup对象
        # print(soup)
        soup = delbackground(soup)           # 去掉第一个pre中的背景颜色，并且设置字体和大小。
        soup = delspanfont(soup)             # 去掉所有字体。
        clipboard(soup)                      # 写入剪贴板。
        # print(soup)
    except Exception as err:
        print('Error', err)
    else:
        print("OK")
