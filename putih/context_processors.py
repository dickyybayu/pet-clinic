def inject_logged_user(request):
    return {
        'logged_user': request.session.get("logged_user")
    }