# 
from tick.src.tick import (
  _tick_
)
from tick.src.tick import (
  tick
)


#
from aiohttp import web

#
app_tick = web.Application()

#
app_tick.add_routes([

  web.get('/',   _tick_),
  
])
