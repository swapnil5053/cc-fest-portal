import jinja2
from types import SimpleNamespace
import traceback

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), undefined=jinja2.StrictUndefined)
ctx = {
    'request': SimpleNamespace(session={'user': 'tester'}, query_params={'error': '', 'success': ''}),
    'title': 'Test',
    'success': '',
    'error': '',
    'query': '',
    'events': [{'id': 1, 'name': 'Test Event', 'description': 'Desc', 'capacity': 50, 'signed_up': 20, 'fee': 150}],
    'registered_ids': [],
    'ticket': {'name': 'Test Event', 'ticket_code': 'ABC123', 'description': 'Desc', 'fee': 150, 'registered_at': 'May 28'},
    'qr_image': '/static/qr.png',
    'overview': {
        'revenue': 1000,
        'total_registrations': 25,
        'active_users': 12,
        'events': [{'id': 1, 'name': 'Test Event', 'capacity': 50, 'fee': 150}],
        'popular_events': [{'id': 1, 'name': 'Test Event', 'capacity': 50, 'fee': 150, 'registrations': 30}]
    },
    'total': 150,
    'status_code': 500,
    'detail': 'Simulated error for template test'
}
# add convenience fields expected by some templates
ctx['events'][0].update({'registered_at': 'May 28', 'ticket_code': 'ABC123'})

templates = ['base.html','events.html','my_events.html','checkout.html','ticket.html','admin_dashboard.html','admin_login.html','login.html','register.html','error.html']
errors = []
for t in templates:
    try:
        env.get_template(t).render(**ctx)
    except Exception:
        errors.append((t, traceback.format_exc()))

if errors:
    for name, err in errors:
        print('---', name, 'ERROR ---')
        print(err)
else:
    print('OK')
