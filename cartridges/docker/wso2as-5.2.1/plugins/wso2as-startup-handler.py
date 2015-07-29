# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import mdsclient
from plugins.contracts import ICartridgeAgentPlugin
from xml.dom.minidom import parse
import socket
from modules.util.log import LogFactory
import time
import subprocess
import os

class WSO2ASStartupHandler(ICartridgeAgentPlugin):

    def run_plugin(self, values):
        log = LogFactory().get_log(__name__)

        log.info("Disabling git ssl verification...")
        os.environ["GIT_SSL_NO_VERIFY"] = "1"


        log.info("Reading port mappings...")
        port_mappings_str = values["PORT_MAPPINGS"]

        http_proxy_port = None
        https_proxy_port = None
        pt_http_port = None
        pt_https_port = None

        # port mappings format: """NAME:mgt-console|PROTOCOL:https|PORT:4500|PROXY_PORT:9443;
        #                          NAME:pt-http|PROTOCOL:http|PORT:4501|PROXY_PORT:7280;
        #                          NAME:pt-https|PROTOCOL:https|PORT:4502|PROXY_PORT:7243"""

        log.info("Port mappings: %s" % port_mappings_str)
        if port_mappings_str is not None:

            port_mappings_array = port_mappings_str.split(";")
            if port_mappings_array:

                for port_mapping in port_mappings_array:
                    log.debug("port_mapping: %s" % port_mapping)
                    name_value_array = port_mapping.split("|")
                    name = name_value_array[0].split(":")[1]
                    protocol = name_value_array[1].split(":")[1]
                    port = name_value_array[2].split(":")[1]
                    if name == "http-9763" and protocol == "http":
                        http_proxy_port = port
                    if name == "http-9443" and protocol == "https":
                        https_proxy_port = port

        log.info("Catalina http proxy port: %s" % http_proxy_port)
        log.info("Catalina https proxy por: %s" % https_proxy_port)

        if http_proxy_port is not None:
            command = "sed -i \"s/^#CONFIG_PARAM_HTTP_PROXY_PORT.*/CONFIG_PARAM_HTTP_PROXY_PORT = %s/g\" %s" % (http_proxy_port, "/opt/ppaas-configurator-4.1.0-SNAPSHOT/template-modules/wso2as-5.2.1/module.ini")
            p = subprocess.Popen(command, shell=True)
            output, errors = p.communicate()
            log.info("Successfully updated catalina http proxy port: %s in AS template module" % http_proxy_port)

        if http_proxy_port is not None:
            command = "sed -i \"s/^#CONFIG_PARAM_HTTPS_PROXY_PORT.*/CONFIG_PARAM_HTTPS_PROXY_PORT = %s/g\" %s" % (https_proxy_port, "/opt/ppaas-configurator-4.1.0-SNAPSHOT/template-modules/wso2as-5.2.1/module.ini")
            p = subprocess.Popen(command, shell=True)
            output, errors = p.communicate()
            log.info("Successfully updated catalina https proxy port: %s in AS template module" % https_proxy_port)


        # configure server
        log.info("Configuring WSO2 AS...")
        config_command = "python /opt/ppaas-configurator-4.1.0-SNAPSHOT/configurator.py"
        env_var = os.environ.copy()
        p = subprocess.Popen(config_command, env=env_var, shell=True)
        output, errors = p.communicate()
        log.info("WSO2 AS configured successfully")

        # start server
        log.info("Starting WSO2 AS...")

        start_command = "exec ${CARBON_HOME}/bin/wso2server.sh start"
        env_var = os.environ.copy()
        p = subprocess.Popen(start_command, env=env_var, shell=True)
        output, errors = p.communicate()
        log.debug("WSO2 AS started successfully")
