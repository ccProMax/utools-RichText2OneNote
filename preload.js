const { execSync } = require('child_process');

window.handle = function () {
	// const path = __dirname
	// utools.showNotification(path);
	// const cod = `python ${path}/demo.py`
	const cod = `python D:\demo.py`
	// utools.showNotification(cod);
	// utools.copyText(cod);
	const info = execSync(cod)
	// utools.showNotification('OK');
	// utools.copyText(info);
	if (!info.status) {
		utools.showNotification('OK');
		return
	}
	info.stderr.on('data', (data) => {
		utools.copyText(data);   // 将内容放进剪贴板，可用于debug
		utools.showNotification('Error');
	});
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
				utools.showNotification(111);
				window.utools.outPlugin()
			}
		}
	}
}
