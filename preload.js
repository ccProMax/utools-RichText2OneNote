const { execSync } = require('child_process');

window.handle = function () {
	// const path = __dirname
	// utools.showNotification(path);
	// const cod = `python ${path}/demo.py`
	const cod = `python D:\demo.py`
	// utools.showNotification(cod);
	// utools.copyText(cod);
	const info = execSync(cod)
	const str = info.toString();
	utools.showNotification(str);
}


window.exports = {
	"handle": {
		mode: "none",
		args: {
			enter: (action) => {

				window.utools.hideMainWindow()

				info = window.handle();
				// utools.copyText(copyText);   // 将内容放进剪贴板，可用于debug
				// utools.showNotification('OK');
				window.utools.outPlugin()
			}
		}
	}
}
