# 
from tick.src.tick import (
  _tick_,
  tick_all
)


#
from aiohttp import web

#
app_tick = web.Application()

#
app_tick.add_routes([

  web.get('/',   _tick_),
  web.get('/all', tick_all)
  
])
