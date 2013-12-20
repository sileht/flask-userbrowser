# -*- coding: utf-8 -*-
###
#
# Copyright (c) 2012 Mehdi Abaakouk <sileht@sileht.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#
###

import os

venv_path = "./venv"
config = "./userbrowser.cfg"

activate_file = os.path.join(venv_path, 'bin/activate_this.py')
execfile(activate_file, dict(__file__=activate_file))

from userbrowser import app, load_config, init_db
load_config(config)
init_db()
return app
