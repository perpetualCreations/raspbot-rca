#!/bin/bash
sudo rm -rf build/raspbotrca-host/*
sudo cp src/* build/raspbotrca-host/ -r
sudo chmod -R 555 build/raspbotrca-host/DEBIAN/postinst
sudo chmod -R 555 build/raspbotrca-host/DEBIAN/prerm

