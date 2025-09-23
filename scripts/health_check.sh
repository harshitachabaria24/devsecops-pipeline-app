#!/bin/bash
curl -sS -f http://localhost:8080/health || exit 1
