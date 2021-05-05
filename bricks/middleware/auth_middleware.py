from aiohttp import web

def middleware_factory():
    @web.middleware
    async def anthenticated(request, handler):
        resp = await handler(request)
        #TODO create login route that returns a valid token
        if request.headers.get('Authorization') == 'Bearer AuthToken':
           return resp
        return web.Response(text='Forbidden', status='403')
    return anthenticated