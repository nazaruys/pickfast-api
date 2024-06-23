#!/bin/bash

echo "Waiting for MySQL and Web to start..."
./wait-for mysql:3306
./wait-for web:8000

echo "Starting..."
cmd="$@"
exec $cmd