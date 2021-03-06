# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import contextlib
import logging
import os

from pylib.constants import host_paths

_REQUESTS_PATH = os.path.join(
    host_paths.DIR_SOURCE_ROOT, 'third_party', 'requests', 'src')
_APPURIFY_PYTHON_PATH = os.path.join(
    host_paths.DIR_SOURCE_ROOT, 'third_party', 'appurify-python', 'src')

with host_paths.SysPath(_REQUESTS_PATH), (
     host_paths.SysPath(_APPURIFY_PYTHON_PATH)):

  handlers_before = list(logging.getLogger().handlers)

  import appurify.api # pylint: disable=import-error
  import appurify.utils # pylint: disable=import-error

  handlers_after = list(logging.getLogger().handlers)
  new_handler = list(set(handlers_after) - set(handlers_before))
  while new_handler:
    logging.info("Removing logging handler.")
    logging.getLogger().removeHandler(new_handler.pop())

  api = appurify.api
  utils = appurify.utils

# This is not thread safe. If multiple threads are ever supported with appurify
# this may cause logging messages to go missing.
@contextlib.contextmanager
def SanitizeLogging(verbose_count, level):
  if verbose_count < 2:
    logging.disable(level)
    yield True
    logging.disable(logging.NOTSET)
  else:
    yield False

