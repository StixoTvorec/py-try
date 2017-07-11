
;(function() {
    'use strict';
    $(function () {
        const url = (window.location.protocol==="https:"?"wss://":"ws://") + window.location.host + '/ws/';
        const RPC = WSRPC(url, 5000);

        RPC.addRoute('whoAreYou', function (data) {
            return window.navigator.userAgent;
        });

        RPC.addRoute('time', function (data) {
            return window.navigator.userAgent;
        });

        RPC.connect();

        window.r = RPC;
    });
})();
