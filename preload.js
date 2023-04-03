const { exec } = require('child_process');

window.handle = function () {
	const path = __dirname
	// utools.showNotification(path);
	const cod = `python ${path}/demo2.py`
	// utools.showNotification(cod);
	// utools.copyText(cod);
	const info = exec(cod)
	// utools.showNotification('OK');
	// utools.copyText(info);
	info.stdout.on('data', (data) => {
		utools.showNotification('OK');
	});
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

				window.handle();
				// utools.copyText(copyText);   // 将内容放进剪贴板，可用于debug
				

				window.utools.outPlugin()
			}
		}
	}
}
