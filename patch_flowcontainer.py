#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monkey patch flowcontainer 来绕过 tshark 版本检查
"""

import flowcontainer.reader

# 修改版本限制
flowcontainer.reader.__tshark_max_version__ = '5.0.0'

print("Patched flowcontainer: tshark max version set to 5.0.0")
