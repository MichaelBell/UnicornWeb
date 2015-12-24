import unicornhat
import time
import cherrypy
import os
import json
from cherrypy.lib.static import serve_file
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

unicornhat.brightness(0.15)

leds = []
for i in xrange(64):
  leds.append({'id':i, 'r':0, 'g':0, 'b':0})

def pixel(pos, col):
  global leds
  unicornhat.set_pixel(7-pos[0], 7-pos[1], col[0], col[1], col[2])
  leds[pos[0]+pos[1]*8]['r'] = col[0]
  leds[pos[0]+pos[1]*8]['g'] = col[1]
  leds[pos[0]+pos[1]*8]['b'] = col[2]

red = (180,0,0)
green = (0,180,0)
blue = (0,0,255)
yellow = (180, 200, 0)
white = (220,255,240)
purple = (180, 0, 220)
black = (0,0,0)
brown = (130,110,60)

def clear():
  for i in xrange(8):
    for j in xrange(8):
      pixel((i,j), black)

def ball(col):
  clear()
  dcol = [x/2 for x in col]
  for i in xrange(0,4):
    for j in xrange(3-i, 5+i):
      pixel((i,j), col)
      pixel((7-i,j), col)
  pixel((1,1), dcol)
  pixel((6,6), dcol)
  pixel((1,6), dcol)
  pixel((6,1), dcol)
  

web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')

class WebRoot:
  @cherrypy.expose
  def index(self):
    return serve_file(os.path.join(web_dir, 'index.html'))

  @cherrypy.expose
  def ws(self):
      # you can access the class instance through
      handler = cherrypy.request.ws_handler

  @cherrypy.expose
  def leds(self):
    print json.dumps(leds)
    return json.dumps(leds)

lwslist=[]

class LedWebSocket(WebSocket):
  def opened(self):
    global lwslist
    lwslist.append(self)

  def closed(self, code):
    global lwslist
    lwslist.remove(self)

  def received_message(self, data):
    global lwslist
    print data.data
    msg = json.loads(data.data)
    print msg
    if msg['req'] == 'led':
      print "(%d,%d), (%d, %d, %d)" % (msg['id']%8, msg['id']/8, msg['r'], msg['g'], msg['b'])
      pixel((msg['id']%8, msg['id']/8), (msg['r'], msg['g'], msg['b']))
      unicornhat.show()
      for lws in lwslist:
        print "send: " + data.data
        lws.send(data.data)
    if msg['req'] == 'reset':
      if msg['to'] == 'ball':
        ball(red)
      else:
        clear()
      unicornhat.show()
      for id, led in enumerate(leds):
        l = led.copy()
        l['req'] = 'led'
        l = json.dumps(l)
        for lws in lwslist:
          lws.send(l)

if __name__ == '__main__':
  ball(red)
  unicornhat.show()

  cherrypy.server.socket_host = '0.0.0.0'
  WebSocketPlugin(cherrypy.engine).subscribe()
  cherrypy.tools.websocket = WebSocketTool()

  cherrypy.quickstart(WebRoot(), '/', 
    {'/css': {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(web_dir, 'css')},
     '/img': {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(web_dir, 'img')},
     '/js':  {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(web_dir, 'js')},
     '/lib': {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(web_dir, 'lib')},
     '/ws':  {'tools.websocket.on': True,
              'tools.websocket.handler_cls': LedWebSocket}})


