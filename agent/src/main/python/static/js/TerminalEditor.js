/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var TerminalEditor = function () {

    var TERMINAL;
    var SOCKRT;
    var STATUS;

    var init = function (options) {
        // terminado.apply(TerminalEditor);
        Terminal.applyAddon(fit);
        var cols = parseInt(document.documentElement.clientWidth / 9.5, 10)
        var rows = parseInt(document.documentElement.clientHeight / 18, 10)
        TERMINAL = new Terminal({
            cols: cols,
            rows: rows
        }),
            protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://',
            socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + "/websocket/" + options.data;
        SOCKRT = new WebSocket(socketURL);

        if (options.show_banner) {
            TERMINAL.open(document.getElementById(options.id));
            TERMINAL.writeln('欢迎使用iMonitor Web Terminal');
        }

        SOCKRT.addEventListener('open', function () {
            // terminal(socket);
            TERMINAL.writeln('正在连接服务器...');
            SOCKRT.send("size:" + cols + "," + rows);
            TERMINAL.on('data', function (data) {
                console.log(data)
                SOCKRT.send(data);
            });
        });

        SOCKRT.addEventListener("message", function (msg) {
            TERMINAL.write(msg.data);
        });

        SOCKRT.addEventListener('error', function (err) {
            SOCKRT.emit(options.data, '\r\n*** SSH CONNECTION ERROR: ' + err.message + ' ***\r\n');
        });

        SOCKRT.addEventListener('close', function (err) {
            TERMINAL.writeln('服务器连接已经关闭，请检查是否服务器配置出现问题！！！');
            STATUS = false
        });

        TERMINAL.fit();

        // terminal.toggleFullScreen(true);
    }

    var close = function (socket) {
        if (!socket) {
            socket.close()
        } else {
            SOCKRT.close()
        }
    }

    var status = function () {
        return STATUS
    }

    return {
        init: init,
        close: close,
        status: status
    }

}()
