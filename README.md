UnicornWeb
==========

Control a Pimoroni Unicorn HAT from your browser.

!(https://raw.githubusercontent.com/MichaelBell/UnicornWeb/master/UnicornWeb.png)

The client side of this project is based on https://github.com/tinkerlog/node-pixel, but the server is uses ws4py served from CherryPy instead of node.js.

## You need ##

A Raspberry Pi with a Pimoroni Unicorn HAT connected (https://shop.pimoroni.com/products/unicorn-hat)

## Installation ##

First get the unicorn hat working if you haven't already: http://learn.pimoroni.com/tutorial/unicorn-hat/getting-started-with-unicorn-hat

Install cherrypy and ws4py:
```
sudo pip install cherrypy
sudo pip install ws4py
```

Checkout this repo:
```
git checkout https://github.com/MichaelBell/UnicornWeb
```
 
## Run it! ##

```
cd UnicornWeb
sudo python server.py
```

Point your browser to http://ip.of.your.raspi/

Have fun!

## See Also ##

You should also take a look at http://learn.pimoroni.com/tutorial/unicorn-hat/getting-started-with-unicorn-paint - I put this together mostly because I didn't find that project :)
