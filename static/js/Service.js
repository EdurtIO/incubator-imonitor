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
let Service = function () {

    var init = function () {
        console.log('init Service')
        initDom()
    }

    var initDom = function () {
        console.log('init dom ...')
        initCompileWay($('input[name="compile_way"]:checked').val())
        initEvent()
    }

    var initEvent = function () {
        $('input[name="compile_way"]').change(function () {
            initCompileWay($(this).val());
        });
        initValidator();
    }

    var initValidator = function () {
        $('#form').bootstrapValidator({
            live: 'enabled',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {}
        }).on('success.form.bv', function (e) {
            e.preventDefault();
            alert(1);
            // $.ajax( ... );
        });
    }

    var initCompileWay = function (value) {
        switch (value) {
            case '0':
                $('#source_git').show()
                $('#source_git_username').show()
                $('#source_git_password').show()
                $('#download').hide()
                break
            case '1':
                $('#source_git').hide()
                $('#source_git_username').hide()
                $('#source_git_password').hide()
                $('#download').show()
                break
        }
    }

    return {
        init: init,
    }

}()

Service.init()