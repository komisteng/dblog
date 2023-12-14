import hashlib
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .models import User,Blog
from django.http import JsonResponse
import markdown

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        birth = request.POST['birth']
        mail = request.POST['mail']
        gender = request.POST['gender']
        bilibili_id = request.POST['bilibili_id']
        
        # 检查邮箱是否已存在
        if User.objects.filter(mail=mail).exists():
            return render(request, 'register.html', {'error': '该邮箱已被注册'})
        
        # 对密码进行SHA256加密
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # 创建用户
        login_user = User(username=username, password=hashed_password, birth=birth, mail=mail, gender=gender, bilibili_id=bilibili_id)
        login_user.save()
        
        request.session['user_id'] = login_user.id
        
        return redirect('profile_tmp')
    
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        
        try:
            # 根据邮箱获取用户
            login_user = User.objects.get(mail=mail)
            
            # 验证密码是否正确
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == login_user.password:
                # 登录成功，将用户信息存储到session中
                request.session['user_id'] = login_user.id
                return redirect('profile_tmp')
            else:
                return render(request, 'login.html', {'error': '邮箱或密码错误'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': '用户不存在'})
    
    return render(request, 'login.html')

def profile_tmp(request):
    user_id = request.session.get('user_id')
    if user_id:
        return redirect("profile", user_id=user_id)
    else:
        return redirect('login')

def profile(request, user_id=None):
    if not user_id:
        user_id = request.session.get('user_id')

    if user_id:
        try:
            user = User.objects.get(id=user_id)
            blogs = Blog.objects.filter(poster=user).order_by('-id')  # 获取该用户发布的博客，按照id降序排序
            paginator = Paginator(blogs, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'profile.html', {'user': user, 'page_obj': page_obj})
        except User.DoesNotExist:
            redirect("profile_tmp")

    # 用户不存在时返回错误信息或重定向到登录页面
    return render(request, 'error.html', {'message': '用户不存在'})




def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    
    return redirect('login')

def main_view(request):
    blogs = Blog.objects.order_by('-upload_date')
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取最近注册的用户
    users = User.objects.order_by('-register_date')[:10]
    return render(request, 'main.html', {'page_obj': page_obj, 'users': users})

def low_auth(request,reason=None):
    error = '通常这个界面不会显示。你可以试试看回到上一个页面'
    if reason == 'need_auth':
        error = "权限不够。"
    elif reason == "no_login":
        error = '用户未登录'
    return render(request, 'low_auth.html', {'error': error})

def upload(request):
    if not request.session.get('user_id'):
        return redirect('low_auth', reason='no_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        poster = request.session.get('user_id')
        blog = Blog(title=title, body=body, poster_id=poster)
        blog.save()
        return redirect('main')  # 重定向到博客列表页面

    return render(request, 'upload.html')
    
def page_view(request, id):
    blog = get_object_or_404(Blog, id=id)
    print(blog.body)
    content = markdown.markdown(blog.body)
    return render(request, 'page.html', {'blog':blog,'content': content})

def all_pages(request):
    blogs = Blog.objects.order_by('id')  # 根据id升序排序
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all.html', {'page_obj': page_obj})



def blog_delete(request,blog_id=None):
    Blog.objects.filter(id=blog_id).delete()
    return redirect('/profile')

def blog_update(request,blog_id=None):
    if request.method == 'GET':
        blog= Blog.objects.filter(id=blog_id).first()
        return render(request, 'blog_update.html', {"blog" : blog})
    title = request.POST.get('title')
    body = request.POST.get('body')
    Blog.objects.filter(id=blog_id).update(title=title,body=body)
    return redirect('/profile')

def user_update(request):
    if not request.session.get('user_id'):
        return redirect('low_auth', reason='no_login')

    user_id = request.session.get('user_id')
    if request.method == 'GET':
        user=User.objects.filter(id=user_id).first()
        return render(request, 'user_update.html', {"user" : user})

    username = request.POST.get("username")
    birth = request.POST.get("birth")
    gender = request.POST.get("gender")
    bilibili_id = request.POST.get("bilibili_id")
    
    User.objects.filter(id=user_id).update(username=username, birth=birth, gender=gender, bilibili_id=bilibili_id)
    return redirect('/profile')