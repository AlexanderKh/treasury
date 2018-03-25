import twitter
import pytz
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
utc = pytz.UTC

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

api = twitter.Api(consumer_key='EWVIrVaIze0LGpd0MssBlQJOm',
                  consumer_secret='6NMZFR77TqgpVgryhiOhSQdb2AXxB4CBG4grsuzrKqNXuf6u3f',
                  access_token_key='935216169543446530-i6N9CurSUGsbrjb99LCeL9q0GYSP1pY',
                  access_token_secret='vArRR61ETZMjsc9253kJojqr0JRnsjbsCP91NgnOexoAj')

user = '<username here>'
limit_reached = False
start_period = datetime(2018, 2, 16).replace(tzinfo=utc)
end_period = datetime(2018, 2, 28).replace(tzinfo=utc)
max_id = None
get_by = 200

to_render = []

while not limit_reached:
    statuses = api.GetUserTimeline(screen_name=user, max_id=max_id, include_rts=False, count=get_by)
    for status in statuses:
        created_at = status.created_at
        print(created_at)
        created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')

        if created_at > end_period: continue
        if created_at < start_period:
            limit_reached = True
            break

        id = status.id_str
        text = status.text
        attachments = []
        for media in status.media or []:
            if media.type != 'photo': continue
            attachments.append(media.media_url)

        to_render.append({'id': id, 'created_at': created_at, 'text': text, 'attachments': attachments})
        print(created_at)

    new_max_id = (len(statuses) > 0) and statuses[-1].id_str
    print(new_max_id)
    print(len(to_render))
    if not new_max_id or new_max_id == max_id: limit_reached = True
    max_id = new_max_id

rendered = template.render(items=to_render)

with open("rendered.html", "wb") as fh:
    fh.write(rendered.encode('utf8'))
