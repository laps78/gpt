#!/bin/bash

# Проверяем операционную систему
if [[ "$OSTYPE" == "linux-gnu" ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    sudo apt-get install git
  else
    echo 'Git уже установлен.' >&2
  fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    brew install git
  else
    echo 'Git уже установлен.' >&2
  fi
elif [[ "$OSTYPE" == "cygwin" ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    choco install git
  else
    echo 'Git уже установлен.' >&2
  fi
elif [[ "$OSTYPE" == "msys" ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    choco install git
  else
    echo 'Git уже установлен.' >&2
  fi
elif [[ "$OSTYPE" == "win32" ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    choco install git
  else
    echo 'Git уже установлен.' >&2
  fi
elif [[ "$OSTYPE" == "freebsd"* ]]; then
  # Проверяем, установлен ли git
  if ! [ -x "$(command -v git)" ]; then
    echo 'Git не установлен. Устанавливаем...' >&2
    sudo pkg install git
  else
    echo 'Git уже установлен.' >&2
  fi
else
  echo 'Операционная система не поддерживается.' >&2
fi
