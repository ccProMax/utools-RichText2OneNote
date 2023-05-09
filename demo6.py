# 主要针对公司里的idea。
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
    div_tag = soup.find('div')   # find是找第一个，如果没有就直接返回了。主要影响idea的第一个div
    # 获取style属性
    if div_tag:
        style_str = div_tag.get('style')
    else:
        return soup
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
    jishu = 0
    # 找到所有的span标签
    span_tags = soup.find_all('span')
    # 遍历所有的span标签
    for span_tag in span_tags:
        # 获取style属性
        # print(span_tag)
        style_str = span_tag.get('style')
        # 将style属性解析为字典
        style_dict = {}
        if style_str:
            for style in style_str.split(';'):
                if style:
                    key, value = style.split(':')
                    style_dict[key.strip()] = value.strip()
            # 移除font-family属性，再将属性设置为'Consolas'
            for i in style_dict.copy():
                if i != "color":
                    del style_dict[i]
            if 'font-family' in style_dict:
                del style_dict['font-family']
            # style_dict['font-size'] = '14px'
            style_dict['font-family'] = 'Consolas'
            jishu += 1   # debug用的，计数，看看一共换了几次字体，这个会影响整个html长度导致后面出问题。
            # 将字典转换为字符串
            new_style_str = '; '.join(
                [f'{key}: {value}' for key, value in style_dict.items()])
            # 将新的style属性设置回span标签
            span_tag['style'] = new_style_str
    # print(jishu)
    return soup


# 删除来自连接，重置头部内容的长度。
def remove_source_url(soup):
    # 重新定义了头部内容。因为len(soup)长度和EndHTML的值不是同一个，所以有bug。
    def head(soup):
        headstr = soup.contents[0].string
        newstr = ''
        lists1 = headstr.split("\n")
        for i in lists1:
            if len(i) < 5:
                continue
            j = i.split(":")
            if j[0] == "StartHTML" or j[0] == "StartFragment":
                j[1] = "0000000131"
            if j[0] == "SourceURL":
                j[1] = "about:blank"
            newstr += j[0]+":"+j[1] + "\n"
        if "SourceURL" not in newstr:
            newstr += "SourceURL:about:blank\n"
        return newstr

    headstr = head(soup)
    newsoup = BeautifulSoup(headstr, "html.parser")
    soup.contents[0] = newsoup
    return soup


# 处理换行符
def add_br_tags(soup):
    # 找到所有的span标签
    span_tags = soup.find_all('span')
    # 遍历所有的span标签
    a = ''
    for span_tag in span_tags:
        if str(span_tag.text).encode("utf-8") == b'\n':  # 如果是回车
            pass
        if b'\n' in str(span_tag.text).encode("utf-8"):
            new_div_tag = soup.new_tag('br')  # 创建一个新的div标签
            span_tag.insert_after(new_div_tag)  # 在找到的位置后面插入新的div标签
            # span_tag.insert_before(new_div_tag)  # 在找到的位置前面插入新的div标签
        a += span_tag.text
        print(span_tag.text)
    # print(a)
    print(soup)
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
        # print(f"原本的长度：{len(soup.prettify())}")
        soup = delbackground(soup)           # 去掉所有的背景颜色
        # 设置第一个div里面的字体为consolas，字体大小为14px。在idea中复制背景内容就会在第一个div中，主要针对idea。
        # soup = fontSize(soup)
        # 遍历所有span标签，如果里面定义了字体，那么就把它定义的字体改为consolas。
        soup = delspanfont(soup)
        soup = add_br_tags(soup)             # 处理换行符
        soup = remove_source_url(soup)       # 删除前面带有的SourceURL
        clipboard(soup)                      # 写入剪贴板。
        # print(f"处理后的长度：{len(soup.prettify())}")
        # print(soup)
    except Exception as err:
        print('Error', err)
    else:
        print("OK")
