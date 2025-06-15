@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')
