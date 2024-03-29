# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import logging
import os
import subprocess
import werkzeug

import noblecrm
from noblecrm import http
from noblecrm.tools import misc

_logger = logging.getLogger(__name__)

index_style = """
        <style>
            body {
                width: 480px;
                margin: 60px auto;
                font-family: sans-serif;
                text-align: justify;
                color: #6B6B6B;
            }
            .text-red {
                color: #FF0000;
            }
        </style>
"""
index_template = """
<!DOCTYPE HTML>
<html>
    <head>
        <title>NobleCRM's PosBox</title>
""" + index_style + """
    </head>
    <body>
        <h1>Your PosBox is up and running</h1>
        <p>
        The PosBox is a hardware adapter that allows you to use
        receipt printers and barcode scanners with NobleCRM's Point of
        Sale, <b>version 8.0 or later</b>. You can start an <a href='https://www.infonoble.com/start'>online free trial</a>,
        or <a href='https://www.infonoble.com/page/download'>download and install</a> it yourself.
        </p>
        <p>
        For more information on how to setup the Point of Sale with
        the PosBox, please refer to
        <a href='https://www.infonoble.com/documentation/user/point_of_sale/posbox/index.html'>the manual</a>.
        </p>
        <p>
        To see the status of the connected hardware, please refer 
        to the <a href='/hw_proxy/status'>hardware status page</a>.
        </p>
        <p>
        Wi-Fi can be configured by visiting the <a href='/wifi'>Wi-Fi configuration page</a>.
        </p>
        <p>
        If you need to grant remote debugging access to a developer, you can do it <a href='/remote_connect'>here</a>.
        </p>
        %s
        <p>
        The PosBox software installed on this posbox is <b>version 17</b>,
        the posbox version number is independent from NobleCRM. You can upgrade
        the software on the <a href='/hw_proxy/upgrade/'>upgrade page</a>.
        </p>
        <p>For any other question, please contact the NobleCRM support at <a href='http://www.infonoble.com/help'>www.infonoble.com/help</a>
        </p>
    </body>
</html>

"""


class PosboxHomepage(noblecrm.addons.web.controllers.main.Home):

    def get_hw_screen_message(self):
        return """
<p>
    The activate the customer display feature, you will need to reinstall the PosBox software.
    You can find the latest images on the <a href="http://nightly.infonoble.com/master/posbox/">NobleCRM Nightly builds</a> website.
    Make sure to download at least the version 16.<br/>
    NobleCRM version 11, or above, is required to use the customer display feature.
</p>
"""

    @http.route('/', type='http', auth='none', website=True)
    def index(self):
        #return request.render('hw_posbox_homepage.index',mimetype='text/html')
        return index_template % self.get_hw_screen_message()

    @http.route('/wifi', type='http', auth='none', website=True)
    def wifi(self):
        wifi_template = """
<!DOCTYPE HTML>
<html>
    <head>
        <title>Wifi configuration</title>
""" + index_style + """
    </head>
    <body>
        <h1>Configure wifi</h1>
        <p>
        Here you can configure how the posbox should connect to wireless networks.
        Currently only Open and WPA networks are supported. When enabling the persistent checkbox,
        the chosen network will be saved and the posbox will attempt to connect to it every time it boots.
        </p>
        <form action='/wifi_connect' method='POST'>
            <table>
                <tr>
                    <td>
                        ESSID:
                    </td>
                    <td>
                        <select name="essid">
"""
        try:
            f = open('/tmp/scanned_networks.txt', 'r')
            for line in f:
                line = line.rstrip()
                line = misc.html_escape(line)
                wifi_template += '<option value="' + line + '">' + line + '</option>\n'
            f.close()
        except IOError:
            _logger.warning("No /tmp/scanned_networks.txt")
        wifi_template += """
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        Password:
                    </td>
                    <td>
                        <input type="password" name="password" placeholder="optional"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        Persistent:
                    </td>
                    <td>
                        <input type="checkbox" name="persistent"/>
                    </td>
                </tr>
                <tr>
                    <td/>
                    <td>
                        <input type="submit" value="connect"/>
                    </td>
                </tr>
            </table>
        </form>
        <p>
                You can clear the persistent configuration by clicking below:
                <form action='/wifi_clear'>
                        <input type="submit" value="Clear persistent network configuration"/>
                </form>
        </p>
        <form>
    </body>
</html>
"""
        return wifi_template

    @http.route('/wifi_connect', type='http', auth='none', cors='*', csrf=False)
    def connect_to_wifi(self, essid, password, persistent=False):
        if persistent:
                persistent = "1"
        else:
                persistent = ""

        subprocess.call(['/home/pi/noblecrm/addons/point_of_sale/tools/posbox/configuration/connect_to_wifi.sh', essid, password, persistent])
        return "connecting to " + essid

    @http.route('/wifi_clear', type='http', auth='none', cors='*', csrf=False)
    def clear_wifi_configuration(self):
        os.system('/home/pi/noblecrm/addons/point_of_sale/tools/posbox/configuration/clear_wifi_configuration.sh')
        return "configuration cleared"

    @http.route('/remote_connect', type='http', auth='none', cors='*')
    def remote_connect(self):
        ngrok_template = """
<!DOCTYPE HTML>
<html>
    <head>
        <title>Remote debugging</title>
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script>
           $(function () {
               var upgrading = false;
               $('#enable_debug').click(function () {
                   var auth_token = $('#auth_token').val();
                   if (auth_token == "") {
                       alert('Please provide an authentication token.');
                   } else {
                       $.ajax({
                           url: '/enable_ngrok',
                           data: {
                               'auth_token': auth_token
                           }
                       }).always(function (response) {
                           if (response === 'already running') {
                               alert('Remote debugging already activated.');
                           } else {
                               $('#auth_token').attr('disabled','disabled');
                               $('#enable_debug').html('Enabled remote debugging');
                               $('#enable_debug').removeAttr('href', '')
                               $('#enable_debug').off('click');
                           }
                       });
                   }
               });
           });
        </script>
""" + index_style + """
        <style>
            #enable_debug {
                padding: 10px;
                background: rgb(121, 197, 107);
                color: white;
                border-radius: 3px;
                text-align: center;
                margin: 30px;
                text-decoration: none;
                display: inline-block;
            }
            .centering{
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Remote debugging</h1>
        <p class='text-red'>
        This allows someone to gain remote access to your Posbox, and
        thus your entire local network. Only enable this for someone
        you trust.
        </p>
        <div class='centering'>
            <input type="text" id="auth_token" size="42" placeholder="Authentication Token"/> <br/>
            <a id="enable_debug" href="#">Enable remote debugging</a>
        </div>
    </body>
</html>
"""
        return ngrok_template

    @http.route('/enable_ngrok', type='http', auth='none', cors='*', csrf=False)
    def enable_ngrok(self, auth_token):
        if subprocess.call(['pgrep', 'ngrok']) == 1:
            subprocess.Popen(['ngrok', 'tcp', '-authtoken', auth_token, '-log', '/tmp/ngrok.log', '22'])
            return 'starting with ' + auth_token
        else:
            return 'already running'
