from django.http import HttpRequest


def add(request: HttpRequest, title: str, content: str, status: bool = True) -> None:
    request.session['status'] = 'SUCCESS' if status else 'FAILED'
    request.session['title'] = title
    request.session['content'] = content


def get(request: HttpRequest) -> dict[str, str | None]:
    if status := request.session.get('status'):
        request.session.pop('status')
    if title := request.session.get('title'):
        request.session.pop('title')
    if content := request.session.get('content'):
        request.session.pop('content')
    return {'status': status, 'title': title, 'content': content}
