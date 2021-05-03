# 
from echo.src.echo import (
  _echo_
)
from echo.src.tick import (
  tick
)


#
from aiohttp import web

#
app_echo = web.Application()

#
app_echo.add_routes([

  web.post('/',   _echo_),
  
])
