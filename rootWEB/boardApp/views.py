from django.shortcuts import render , redirect


from .models import *
from django.shortcuts import render ,redirect
from django.http      import JsonResponse

from .models import *

from django.core.paginator import Paginator
# Create your views here.

# M(Model) - data

def main(request) :
    print('>>>> debug , client path : / index, main()call, render /board/index.html')
    # 세션유무에 따른 화면 분기
    if request.session.get('session_user_id') :
        print('>>>>> debug , session exits')
        context = {}
        context['name'] = request.session['session_name']
        context['img'] = request.session['session_img']
        context['user_id'] = request.session['session_user_id']
        return render(request , 'board/main.html' , context)

    return render(request , 'board/index.html')

def login(request) :
    print('>>>> debug , client path : / login, login()call, render /board/index.html')
    # 사용자의 요청방식이 GET | POST 에따라서 달라짐
    # 조건처리하고싶으면 - request.method == 'GET'| request.method == 'POST'
    id  = request.POST['id']
    pwd = request.POST['pwd']
    print('>>>> debug, params' , id , pwd)

    # SQL : select * from table where id = id and pwd = pwd ;
    # ORM(Object Relational Mapping)
    # table(row) == class(instance)
    # return render(request , 'board/index.html')

    user = user_tbl.objects.get(user_id= id, user_pwd= pwd)
    print('>>>> debug , result = ' , user)

    # 데이터를 심는 작업
    # dict 형식으로
    # 세션생성작업
    request.session['session_name'] = user.user_name
    request.session['session_img'] = user.user_img
    request.session['session_user_id'] = user.user_id
    # 세션을 컨텍스트에 심는작업
    context = {}
    context['name']    = request.session['session_name']
    context['img']     = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/main.html' , context)

def logout(request) :
    print('>>>> debug , client path : /logout , logout()call, render / board/index.html')
    # 세션이 남아있다.
    # 세션을 삭제하는 작업이 필요
    request.session['session_name'] = {}
    request.session['session_img'] = {}
    request.session['session_user_id'] = {}
    return redirect('index')

# board : 게시물 목록을 화면에 출력할수 있도록 데이터 베이스로 부터 데이터를 가져와 심고 화면을 분기시킨다.
def list(request) :
    print('>>>> debug , client path : /list , list() call , render / board/index.html')

    # ORM - select * from board_tbl order by id desc ;
    # all() - 전체 데이터 검색
    # order_by() - 정렬(- 내림차순)
    boards = board_tbl.objects.all().order_by('-id')
    print('>>>>> debug , result , type = ' , boards , type(boards))
    ####
    paginator = Paginator(boards, 2)
    page = int(request.GET.get('page', 1))
    board_list = paginator.get_page(page)
    #### has_previous , has_next , count......

    context = { 'boards' : board_list}
    # 세션유지를 위해서 다시한번 심는 작업이 필요함
    context['name']    = request.session['session_name']
    context['img']     = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request , 'board/list.html' , context)

def joinForm(request) :
    print('>>>> debug , client path : /joinForm , joinForm() call , render / board/join.html')
    return render(request, 'board/join.html')

# join함수 호출시 파라미터 값으로 전달된 id, pwd , name 을 디버깅으로 출력한다면?
def join(request) :
    print('>>>> debug , client path : /join , join() call , render/ board/join.html')
    id = request.POST.get('id')
    pwd = request.POST.get('pwd')
    name = request.POST.get('name')
    print('>>>> debug , params = ' , id, pwd , name)

    # ORM : table == class(instance)
    # insert into tabe;(column) values(id, pwd, name)
    # save(), create()
    user_tbl(user_id = id , user_pwd = pwd , user_name = name , user_img = 'boy.png').save()

    return  redirect('index')

def registerForm(request):
    print('>>>> debug , client path : /bbsForm , register() call , render/ board/register.html')

    # 데이터 공유작업 고민하기

    context = {}
    # 세션유지를 위해서 다시한번 심는 작업이 필요함
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request , 'board/register.html' , context)

# board_tbl : insert ~~
# writer 외래키인데 장고 ORM에서 외래키 값은 부모의 객체가 삽입되어야 한다.
# list 로 이동하여 입력한 게시물 정보가 출력되도록 구현!!!
def register(request) :
    print('>>>> debug , client path : /register , register() call , redirect list')
    title = request.POST.get('title')
    content = request.POST.get('content')
    writer = request.POST.get('writer')
    print('>>>> debug , params = ', title, content, writer)

    # ORM
    # select
    user = user_tbl.objects.get(user_id=writer)
    board_tbl(title = title , content = content , writer = user).save()

    return redirect('list')

# 게시글의 식별번혼 id를 파라미터로 받아서
# 해당 게시글의 정보를 디비에서 select 후 context 심어서
# 화면을 렌더링 - read.html
def read(request):
    print('>>>> debug , client path : /view , read() call , render board/read.html')
    id = request.GET.get('id')

    # ORM : select * from board_tbl where id = ?
    board = board_tbl.objects.get(id = id)

    board.viewcnt = board.viewcnt + 1
    board.save()

    context = {'board': board }
    # 세션유지를 위해서 다시한번 심는 작업이 필요함
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/read.html', context)
# 게시글의 식별번호 id를 파라미터로 받아서
# 해당 게시글을 삭제하고 redirect 이용한 요청 재지정 list 이동하는 것
# table == class
# orm : get(id = id).delete()
def delete(request):
    print('>>>> debug , client path : /delete , delete() call , redirect list')
    id = request.GET.get('id')

    board_tbl.objects.get(id = id).delete()

    return redirect('list')

def update(request) :
    print('>>>>> debug , client path : update , update() call , redirect view')
    title   = request.GET.get('title')
    content = request.GET.get('content')
    id      = request.GET.get('id')



    board = board_tbl.objects.get(id=id)
    board.title = title
    board.content = content
    board.save()
    return redirect('list')


def search(request):
    print('>>>> debug , client path : /search , search() call , ajax JsonResponse ')
    type   = request.POST.get('searchType')
    keyword= request.POST.get('searchKeyword')
    print('>>>>> debug , param = ' , type , keyword)

    if type == 'title' :
        boards = board_tbl.objects.filter(title__icontains=keyword)
    elif type == 'writer' :

        boards = board_tbl.objects.filter(writer_id=keyword)

    print('>>>>> debug , result len - ' , len(boards))
    response_json = []
    for board in boards :
        response_json.append({
            'id'      : board.id,
            'title'   : board.title,
            'writer'  : board.writer.user_id,
            'regdate' : board.regdate,
            'viewcnt' : board.viewcnt
        })
    print('>>>> json data = ' , response_json)
    return JsonResponse(response_json , safe=False)