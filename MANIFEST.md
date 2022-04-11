title: GuiMRadio
brief: Collection of custom blocks for radio decoding
tags: # Tags are arbitrary, but look at CGRAN what other authors are using
  - sdr
author:
  - Guilhem Tiennot <contact@tiennotblog.fr>
copyright_owner:
  - Guilhem Tiennot
license:
gr_supported_version: 3.9 # Put a comma separated list of supported GR versions here
#repo: # Put the URL of the repository here, or leave blank for default
#website: <module_website> # If you have a separate project website, put it here
#icon: <icon_url> # Put a URL to a square image here that will be used as an icon on CGRAN
---
This package includes:
  - Manchester and NRZ decoding block
  - A Raspberry Pi GPIO sink block
  - Some OTP sinks, that can send commands, trigger GPIO or send serial data
  when activated.
