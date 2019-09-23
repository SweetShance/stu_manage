"""
中间件:
    1.
    2. 基于角色的权限管理路由访问
"""
from django.shortcuts import redirect, HttpResponse, render
from django.utils.deprecation import MiddlewareMixin
import re

class MyMiddleware(MiddlewareMixin):
    # 请求
    def process_request(self, request):
        # 获取当前请求的路由
        request_url = request.path
        # 设置路由白名单,任何人可以访问, 登录注册 和 后台登录
        valid_urls = ['/', '/admin/(.*)', '/error',]
        for url in valid_urls:
            result = re.match("^%s$"%url, request_url)
            if result:
                return None
        # # 登录访问限制, 获取session 中的值
        user_id = request.session.get('user', [])
        if not user_id:
            return redirect('/')
        
        # 根据权限设置登录用户有没有权限
        permission = request.session.get('permission_list').get(request_url)
        # print(request_url)
        from_url = request.META.get('HTTP_REFERER',"/")
        if not permission:
            if '/index' in from_url:
               return redirect('/error?from_url=%s'%'/welcome') 
            return redirect('/error?from_url=%s'%from_url)
            

    # 
    def process_response(self, request, response):
        return response