const { exec } = require('child_process');

window.handle = function () {
	const path = __dirname
	const cod = `python ${path}/demo.py`
	const info = exec(cod)
	// utools.copyText(cod);
	info.stdout.on('data', (data) => {
		// utools.showNotification(data);
	});
	info.stderr.on('data', (data) => {
		utools.copyText(data);   // 将内容放进剪贴板，可用于debug
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
				utools.showNotification('OK');

				window.utools.outPlugin()
			}
		}
	}
}
