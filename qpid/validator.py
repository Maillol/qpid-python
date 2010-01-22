#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

class Values:

  def __init__(self, *values):
    self.values = values

  def validate(self, o):
    if not o in self.values:
      return "%s not in %s" % (o, self.values)

  def __str__(self):
    return self.value

class Types:

  def __init__(self, *types):
    self.types = types

  def validate(self, o):
    for t in self.types:
      if isinstance(o, t):
        return
    if len(self.types) == 1:
      return "%s is not a %s" % (o, self.types[0].__name__)
    else:
      return "%s is not one of: %s" % (o, ", ".join([t.__name__ for t in self.types]))

class Map:

  def __init__(self, map, restricted=True):
    self.map = map
    self.restricted = restricted

  def validate(self, o):
    errors = []

    if not hasattr(o, "get"):
      return "%s is not a map" % o

    for k, t in self.map.items():
      v = o.get(k)
      if v is not None:
        err = t.validate(v)
        if err: errors.append("%s: %s" % (k, err))
    if self.restricted:
      for k in o:
        if not k in self.map:
          errors.append("%s: illegal key" % k)
    if errors:
      return ", ".join(errors)
