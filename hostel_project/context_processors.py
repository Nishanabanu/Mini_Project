def user_name(request):
    return {
        'user_name': request.session.get('user_name', 'Guest')
    }
