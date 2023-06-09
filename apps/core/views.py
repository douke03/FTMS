from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    # POST
    if request.method == "POST":
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get("userid")
        Pass = request.POST.get("password")

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            # ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                auth_login(request, user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse("sample"))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, "core/login.html")


@login_required
# @csrf_exempt
def sample(request):
    params = {
        "UserID": request.user,
    }
    return render(request, "core\sample.html", context=params)
