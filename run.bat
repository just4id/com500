#!/usr/bin/bash

@echo off&SetLocal EnableDelayedExpansion
set page_fid=
FOR /F "delims=" %%a in (page.txt) do python run_scrapy.py !page_fid!  %%a
