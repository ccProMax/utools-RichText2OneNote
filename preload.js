const { execSync } = require('child_process');

window.handle = function () {
	// const path = __dirname
	// utools.showNotification(path);
	// const cod = `python ${path}/demo.py`
	const cod = `python D:\demo.py`          // 直接写死目录算了，执行D盘的demo.py
	// utools.showNotification(cod);
	// utools.copyText(cod);
	const info = execSync(cod)
	const str = info.toString();  // info是串数字，转换为字符串才能知道是什么
	utools.showNotification(str);  // 正常输出OK，这里显示的就是OK
	if (str.length != 4) {         // 长度不等于4，也就是不是OK，就有问题，就把输出的问题放到剪贴板中。
		utools.copyText(str);
	}
}


window.exports = {
	"handle": {
		mode: "none",
		args: {
			enter: (action) => {

				window.utools.hideMainWindow()

				window.handle();
				// utools.copyText(copyText);   // 将内容放进剪贴板，可用于debug
				// utools.showNotification('OK');
				window.utools.outPlugin()
			}
		}
	}
}
