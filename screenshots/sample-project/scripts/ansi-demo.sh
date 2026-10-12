#!/usr/bin/env bash
# Prints the 16 ANSI colours for eyeballing terminal theming.
for i in {0..15}; do
  printf '\033[48;5;%dm %2d \033[0m' "$i" "$i"
done
printf '\n'
for code in 30 31 32 33 34 35 36 37; do
  printf '\033[%smcolour %s\033[0m\n' "$code" "$code"
done
