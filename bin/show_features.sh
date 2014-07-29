#!/usr/bin/env sh

behave | grep -e "^Feature:" | sed s/^Feature:/-/
echo ""

