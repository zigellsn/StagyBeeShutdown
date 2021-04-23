#  Copyright 2021 Simon Zigelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import os
import random
import string
import sys
from os.path import exists
from subprocess import call
from sys import platform

from twisted.internet import ssl, task, defer, endpoints
from twisted.logger import Logger, globalLogPublisher, textFileLogObserver
from twisted.python.modules import getModule
from twisted.web import server
from twisted.web.resource import Resource

log = Logger()


class Simple(Resource):

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)


class Token(Resource):
    isLeaf = True

    def render_GET(self, request):
        input1 = input(f"{request.client} requests a token. Grant access? [y/N]: ")
        if input1 == "y":
            request.setResponseCode(200)
            return __get_token__()
        else:
            request.setResponseCode(401)
            return b"Not authorized"


class Shutdown(Resource):
    isLeaf = True

    def render_POST(self, request):
        token = request.content.read()
        if not __check_token__(token):
            request.setResponseCode(401)
            return b"Token not valid"

        if platform.startswith("freebsd") or platform.startswith("linux") or platform.startswith(
                "aix") or platform.startswith("cygwin"):
            if os.getenv("RUN_IN_CONTAINER"):
                __write_signal_file__("shutdown_signal", "shutdown")
            else:
                if exists("scripts/shutdown.sh"):
                    call(["sh scripts/shutdown.sh", "-h", "now"], shell=False)
                else:
                    request.setResponseCode(500)
                    return b"Shutdown script not found"
        elif platform.startswith("win32"):
            if exists("scripts/shutdown.bat"):
                call(["scripts/shutdown.bat", "-h"], shell=False)
            else:
                request.setResponseCode(500)
                return b"Shutdown script not found"
        request.setResponseCode(202)
        return b"Shutdown in progress"


class Reboot(Resource):
    isLeaf = True

    def render_POST(self, request):
        token = request.content.read()
        if not __check_token__(token):
            request.setResponseCode(401)
            return b"Token not valid"

        if platform.startswith("freebsd") or platform.startswith("linux") or platform.startswith(
                "aix") or platform.startswith("cygwin"):
            if os.getenv("RUN_IN_CONTAINER"):
                __write_signal_file__("shutdown_signal", "reboot")
            else:
                if exists("scripts/shutdown.sh"):
                    call(["sh scripts/shutdown.sh", "-r"], shell=False)
                else:
                    request.setResponseCode(500)
                    return b"Reboot script not found"
        elif platform.startswith("win32"):
            if exists("scripts/shutdown.bat"):
                call(["scripts/shutdown.bat", "-r"], shell=False)
            else:
                request.setResponseCode(500)
                return b"Reboot script not found"
        request.setResponseCode(202)
        return b"Reboot in progress"


def main(reactor, port, issue_token, certificate):
    if not exists("token"):
        access_rights = 0o755
        try:
            os.mkdir("token", access_rights)
        except OSError:
            print("Creation of the directory 'token' failed")
            exit()
    globalLogPublisher.addObserver(textFileLogObserver(sys.stdout))
    cert_data = getModule(__name__).filePath.sibling(certificate).getContent()
    certificate = ssl.PrivateCertificate.loadPEM(cert_data)

    root = Simple()
    root.putChild(b"shutdown", Shutdown())
    root.putChild(b"reboot", Reboot())
    if issue_token:
        root.putChild(b"token", Token())

    site = server.Site(root)
    endpoint = endpoints.SSL4ServerEndpoint(reactor, port, certificate.options())
    endpoint.listen(site)
    reactor.run()
    return defer.Deferred()


def __write_signal_file__(filename, mode):
    f = open(filename, "w")
    f.write(mode)
    f.close()


def __check_token__(token):
    if exists("token/token"):
        f = open("token/token", "rb")
        my_token = f.read()
        f.close()
        if my_token == token and len(my_token) > 0:
            return True
    return False


def __get_token__():
    if exists("token/token"):
        f = open("token/token", "rb")
        token = f.read()
        f.close()
        if len(token) == 0:
            token = __create_token__()
    else:
        token = __create_token__()
    return token


def __create_token__():
    token = bytes("".join(random.SystemRandom().choice(
        string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits) for _ in range(64)),
                  "utf-8")
    f = open("token/token", "wb")
    f.write(token)
    f.close()
    return token


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("-p", "--port", help="Port", default=8010)
    parser.add_argument("-t", "--token", help="Issue token", action="store_true")
    parser.add_argument("-c", "--certificate", help="Server certificate file", default="server.pem")
    args = parser.parse_args()

    if args.version:
        print("StagyBeeShutdown 0.1.0-alpha01")
        print("Copyright 2021 Simon Zigelli")
        exit()

    task.react(main, (args.port, args.token, args.certificate))
