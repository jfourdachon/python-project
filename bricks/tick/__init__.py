# 
from tick.src.tick import (
  _tick_,
  tick_all,
  plot
)


#
from aiohttp import web

#
app_tick = web.Application()

#
app_tick.add_routes([

  web.get('/',   _tick_),
  web.get('/all', tick_all),
  web.post('/plot', plot)
  
])
