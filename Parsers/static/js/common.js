
; (function() {
    var url = (window.location.protocol==="https:"?"wss://":"ws://") + window.location.host + '/ws/';
    RPC = WSRPC(url, 5000);

    // Инициализируем объект
    RPC.call('test').then(function (data) {
        // посылаем аргументы как *args
        RPC.call('test.serverSideFunction', [1,2,3]).then(function (data) {
            console.log("Server return", data)
        });

        // Объект как аргументы **kwargs
        RPC.call('test.serverSideFunction', {size: 1, id: 2, lolwat: 3}).then(function (data) {
            console.log("Server return", data)
        });
    });

    RPC.addRoute('whoAreYou', function (data) {
        return window.navigator.userAgent;
    });

    RPC.addRoute('time', function (data) {
        return window.navigator.userAgent;
    });

    RPC.connect();
})();
