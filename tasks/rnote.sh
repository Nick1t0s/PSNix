#!/usr/bin/env bash
sudo snap install rnote
snap connect rnote:removable-media 2>/dev/null || true