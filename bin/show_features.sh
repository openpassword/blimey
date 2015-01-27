#!/usr/bin/env sh

behave -d | grep -e "^Feature:" | sed s/^Feature:/-/
echo ""

