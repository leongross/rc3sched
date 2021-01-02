from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/scd')
def schedule():
    return render_template('scd.html')

@app.route('/scd/<string:track>')
def schedule_track_kw(track):
    m   = {
        "com"   : "Community",
        "soc"   : "Ethics, Society \u0026 Politics",
        "its"   : "IT-Security",
        "art"   : "Art \u0026 Culture",
        "hwm"   : "Hardware \u0026 Making",
        "fsc"   : "Fireside Chat",
        "sci"   : "Science",
        "xxx"   : "null",
        "oth"   : "Other"
    }

    if track in m:
        print(m[track])
        r       = requests.get('https://fahrplan.events.ccc.de/rc3/2020/Fahrplan/schedule.json').json()
        days    = r['schedule']['conference']['days']
        t       = []

        for day in days:
            rooms   = day['rooms']
            rl      = ['rC1', 'rC2', 'chaosstudio-hamburg', 'restrealitaet']
            rs      = [ rooms[x] for x in rl ]
            
            for rr in rs:
                for e in rr:
                    if e['track'] == m[track]:
                        e['date'] = day['date']
                        t.append(e)

    else:
        return render_template('track_not_found.html')

    return render_template('track.html', l = [parse_event(x) for x in t], short = track, long = m[track])


def parse_event(e:dict):
    return [
        e['date'],
        e['start'],
        e['duration'],
        e['track'],
        e['language'],
        e['url']
    ]

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.register_error_handler(404, not_found)
