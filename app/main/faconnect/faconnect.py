import os
import sys
import re
import time
from collections import OrderedDict
import getpass
import logging
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%y%m%d %H%M%S")
LOGGER = logging.getLogger(__name__)
lock = threading.Lock()


class FAConnect:
    AEL_PYTHON_PATH = ""
    INI_FILE_PATH = ""

    # Regular expressions for parsing section headers and options.
    DEFAULTSECT = "DEFAULT"
    SECTCRE = re.compile(
        r'\['  # [
        r'(?P<header>[^]]+)'  # very permissive!
        r'\]'  # ]
    )
    OPTCRE = re.compile(
        r'(?P<option>[^:=\s][^:=]*)'  # very permissive!
        r'\s*(?P<vi>[:=])\s*'  # any number of space/tab,
        # followed by separator
        # (either : or =), followed
        # by any # space/tab
        r'(?P<value>.*)$'  # everything up to eol
    )
    OPTCRE_NV = re.compile(
        r'(?P<option>[^:=\s][^:=]*)'  # very permissive!
        r'\s*(?:'  # any number of space/tab,
        r'(?P<vi>[:=])\s*'  # optionally followed by
        # separator (either : or
        # =), followed by any #
        # space/tab
        r'(?P<value>.*))?$'  # everything up to eol
    )
    tries = 0

    def __init__(self, env_name=None, username=None, password=None, archive_mode=False, historical_date=None, date_today=None):

        self.config_handler = None
        self.principal = None
        self.session = None
        self.app = None
        self.amas_pass = None
        self._sections = OrderedDict()
        self._dict = OrderedDict
        self._defaults = OrderedDict()
        self._optcre = self.OPTCRE
        self.archive = archive_mode
        self.historical_date = historical_date
        self.date_today = date_today
        self.ads_url = None

        self.server = os.environ["FRONT_SERVER"]
        self.port = os.environ["FRONT_PORT"]
        self.single_sign_on = bool(os.environ["SSO"])
        self.env_name = os.environ["FRONT_ENVIRONMENT"] if not env_name else env_name
        self.password = os.environ["PASSWORD"] if not self.single_sign_on else None
        self.username = os.environ["USERNAME"]
        self.ael_python_path = os.environ["AEL_PYTHON_PATH"]
        self.ini_file_path = os.environ["INI_FILE_PATH"]

        FAConnect.AEL_PYTHON_PATH = self.ael_python_path
        sys.path.append(self.ael_python_path)

        if username:
            self.username = username
        if not username and self.single_sign_on:
            self.username = getpass.getuser()

        if password:
            self.password = password

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import acm
        is_connected = acm.IsConnected()
        tries = 0
        while is_connected:
            acm.Disconnect()
            time.sleep(10)
            tries += 1
            is_connected = acm.IsConnected()
        LOGGER.info("Disconnected from {} Front, {} Tries".format(self.username, tries))

    def disconnect(self):
        import acm
        is_connected = acm.IsConnected()
        tries = 0
        while is_connected:
            acm.Disconnect()
            time.sleep(10)
            tries += 1
            is_connected = acm.IsConnected()
        LOGGER.info("Disconnected from {} Front, {} Tries".format(self.username, tries))

    def _ads_url(self):
        if self.env_name:
            self.ads_url = self.get_ads_url()
        elif self.server and self.port:
            self.ads_url = "{}:{}".format(self.server, self.port)
        else:
            raise ValueError("No server/environment provided")

    def connect(self):
        self._ads_url()
        import acm
        import ael

        LOGGER.info("About to connect")

        if self.date_today:
            ael.date_today = self.date_today
            acm.Time.SetDateToday(self.date_today)
        if self.historical_date:
            ael.historical_date = self.historical_date
            acm.Time.SetHistoricalDate(self.historical_date)

        if self.password:
            self.single_sign_on = False
        con = acm.Connect(self.ads_url, self.username, self.password, self.amas_pass, self.app, self.archive, self.session,
                          self.principal, self.config_handler, self.single_sign_on)

        LOGGER.info("Connected to {} with User {}\n".format(self.env_name, self.username))

    def connection_status(self):
        import acm
        is_connected = acm.IsConnected()
        if is_connected:
            info = {
                "is-connected": acm.IsConnected(),
                "environment": self.env_name
            }
        else:
            info = {
                "is-connected": acm.IsConnected()
            }
        return info

    def load_config(self):
        with open(self.ini_file_path, 'rU') as fin:
            self._read(fin, fin.name)
        return None

    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
            """
        cursect = None  # None, or a dictionary
        optname = None
        lineno = 0
        e = None  # None, or an exception
        while True:
            line = fp.readline()
            # print("line - ", line)
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname].append(value)
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == self.DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        cursect['__name__'] = sectname
                        self._sections[sectname] = cursect
                    # So sections can'trade start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise Exception(fpname, lineno, line)
                # an option line?
                else:
                    mo = self._optcre.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        optname = optname.rstrip().lower()
                        # This check is fine because the OPTCRE cannot
                        # match if it would set optval to None
                        if optval is not None:
                            if vi in ('=', ':') and ';' in optval:
                                # ';' is a comment delimiter only if it follows
                                # a spacing character
                                pos = optval.find(';')
                                if pos != -1 and optval[pos - 1].isspace():
                                    optval = optval[:pos]
                            optval = optval.strip()
                            # allow empty values
                            if optval == '""':
                                optval = ''
                            cursect[optname] = [optval]
                        else:
                            # valueless option handling
                            cursect[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = Exception(fpname)
                        e.append(lineno, repr(line))

        # if any parsing errors occurred, raise an exception
        if e:
            raise e

        # join the multi-line values collected while reading
        all_sections = [self._defaults]
        all_sections.extend(self._sections.values())

        for options in all_sections:
            # print("options", options)
            for name, val in options.items():
                if isinstance(val, list):
                    options[name] = '\n'.join(val)

    def get(self, section, option):
        opt = option.lower()
        if section not in self._sections:
            if section != self.DEFAULTSECT:
                raise Exception(section)
            if opt in self._defaults:
                return self._defaults[opt]
            else:
                raise Exception(option, section)
        elif opt in self._sections[section]:
            return self._sections[section][opt]
        elif opt in self._defaults:
            return self._defaults[opt]
        else:
            raise Exception(option, section)

    def get_ads_url(self):
        self.load_config()
        return self.get('ADS.' + self.env_name, "serveraddress")

    def execute(self, *args):
        raise NotImplementedError("No implementation found")

    def is_connected(self):
        import acm
        return acm.IsConnected()