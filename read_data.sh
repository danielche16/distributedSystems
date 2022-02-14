#!/bin/bash

file1=$(curl -L http://localhost:8000/log-sensor1)
echo $file1 >> website_data.txt