# Home Assistant Duka Smartfan Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This is a Duka Smartfan custom component for Home Assistant.

Forked from and heavily inspired by the great [dingusdk ha-dukaone package](https://github.com/dingusdk/ha-dukaone) for connecting with a Duka One.

To use it, the easist way is to install it with [HACS](https://hacs.xyz). Add this repo as a Custom Repository in HACS and install it.

Without HACS you will have to place the custom_components folder in your HA configuration folder.

To add a Duka Smartfan to Home assistant go to configuration|Integrations and click the "+" in the lower right corner. Then find the "Duka Smartfan" in the list.

In the dialog enter a name for the device and the device id. You can find the device id in the mobile app for Duka One. If you know the IP of the device you can enter it. Or you can enter the broardcast address of your subnet (like 192.168.0.255). You can also leave it empty and the integration will try to broadcast and find the device. (Note this does not always works - depending on you network and Home Assistant setup). 

## License

HA-DukaSmartfan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

HA-DukaSmartfan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DukaSmartfan. If not, see <http://www.gnu.org/licenses/>.
