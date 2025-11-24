from flask import Flask, render_template, request, redirect, flash
from db_config import get_db
from datetime import datetime, timedelta
import os
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

@app.route("/")
def home():
    return redirect("/events")



@app.route("/events")
def events():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Event ORDER BY start_time ASC")
    events = cur.fetchall()
    edit_id = request.args.get('edit_id')
    edit_event = None
    if edit_id:
        cur.execute("SELECT * FROM Event WHERE event_id=%s", (edit_id,))
        edit_event = cur.fetchone()
    return render_template("events.html", events=events, edit_event=edit_event)


@app.route("/add_event", methods=["POST"])
def add_event():
    title = request.form.get("title")
    start = request.form.get("start_time")
    end = request.form.get("end_time")
    if not title or not start or not end:
        return redirect('/events')

    db = get_db()
    cur = db.cursor()
    event_id = request.form.get('event_id')
    if event_id:
        cur.execute("""
            UPDATE Event SET title=%s, start_time=%s, end_time=%s
            WHERE event_id=%s
        """, (title, start, end, event_id))
        flash('Event updated.', 'success')
    else:
        cur.execute("""
            INSERT INTO Event (title, start_time, end_time)
            VALUES (%s, %s, %s)
        """, (title, start, end))
        flash('Event created.', 'success')

    db.commit()
    return redirect('/events')



@app.route("/resources")
def resources():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Resource")
    resources = cur.fetchall()
    edit_id = request.args.get('edit_id')
    edit_resource = None
    if edit_id:
        cur.execute("SELECT * FROM Resource WHERE resource_id=%s", (edit_id,))
        edit_resource = cur.fetchone()
    return render_template("resources.html", resources=resources, edit_resource=edit_resource)


@app.route("/add_resource", methods=["POST"])
def add_resource():
    name = request.form.get("resource_name")
    rtype = request.form.get("resource_type")
    if not name or not rtype:
        return redirect('/resources')

    db = get_db()
    cur = db.cursor()
    resource_id = request.form.get('resource_id')
    if resource_id:
        cur.execute('UPDATE Resource SET resource_name=%s, resource_type=%s WHERE resource_id=%s', (name, rtype, resource_id))
        flash('Resource updated.', 'success')
    else:
        cur.execute("""
            INSERT INTO Resource (resource_name, resource_type)
            VALUES (%s, %s)
        """, (name, rtype))
        flash('Resource added.', 'success')
    db.commit()
    return redirect('/resources')


@app.route("/deallocate_resource/<int:allocation_id>")
def deallocate_resource(allocation_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM EventResourceAllocation WHERE allocation_id=%s", (allocation_id,))
    db.commit()
    flash('Allocation removed.', 'success')
    return redirect("/allocate")


@app.route("/deallocate_all_resources/<int:event_id>")
def deallocate_all_resources(event_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM EventResourceAllocation WHERE event_id=%s", (event_id,))
    db.commit()
    flash('All allocations removed for this event.', 'success')
    return redirect("/allocate")


@app.route("/allocate", methods=["GET", "POST"])
def allocate():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM Event")
    events = cur.fetchall()

    cur.execute("SELECT * FROM Resource")
    resources = cur.fetchall()

    cur.execute("""
        SELECT a.allocation_id, e.event_id, e.title AS event_title,
               r.resource_id, r.resource_name, r.resource_type
        FROM EventResourceAllocation a
        JOIN Event e ON a.event_id = e.event_id
        JOIN Resource r ON a.resource_id = r.resource_id
        ORDER BY e.start_time ASC
    """)
    allocations = cur.fetchall()

    edit_id = request.args.get('edit_id')
    edit_alloc = None
    if edit_id:
        cur.execute('SELECT * FROM EventResourceAllocation WHERE allocation_id=%s', (edit_id,))
        edit_alloc = cur.fetchone()

    if request.method == "POST":
        event_id = request.form["event_id"]
        resource_id = request.form["resource_id"]
        allocation_id = request.form.get('allocation_id')

        cur.execute("SELECT start_time, end_time FROM Event WHERE event_id = %s", (event_id,))
        event_time = cur.fetchone()
        start_time = event_time["start_time"]
        end_time = event_time["end_time"]

        cur.execute("""
            SELECT a.allocation_id, e.event_id, e.start_time, e.end_time
            FROM EventResourceAllocation a
            JOIN Event e ON a.event_id = e.event_id
            WHERE a.resource_id = %s
              AND e.start_time < %s
              AND e.end_time > %s
        """, (resource_id, end_time, start_time))

        conflict = cur.fetchone()

        if conflict:
            flash('⚠ This resource is already allocated for this time slot!', 'error')
            return redirect('/allocate')

        if allocation_id:
            cur.execute('UPDATE EventResourceAllocation SET event_id=%s, resource_id=%s WHERE allocation_id=%s', (event_id, resource_id, allocation_id))
            flash('Allocation updated.', 'success')
        else:
            cur.execute("""
                INSERT INTO EventResourceAllocation (event_id, resource_id)
                VALUES (%s, %s)
            """, (event_id, resource_id))
            flash('Resource allocated.', 'success')
        db.commit()

        return redirect("/allocate")

    return render_template("allocate.html", events=events, resources=resources, allocations=allocations, edit_alloc=edit_alloc)


@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM EventResourceAllocation WHERE event_id=%s', (event_id,))
    cur.execute('DELETE FROM Event WHERE event_id=%s', (event_id,))
    db.commit()
    flash('Event deleted.', 'success')
    return redirect('/events')


@app.route('/delete_resource/<int:resource_id>')
def delete_resource(resource_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM EventResourceAllocation WHERE resource_id=%s', (resource_id,))
    cur.execute('DELETE FROM Resource WHERE resource_id=%s', (resource_id,))
    db.commit()
    flash('Resource deleted.', 'success')
    return redirect('/resources')

@app.template_global()
def format_time_with_ampm(value):
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except Exception:
            return value
    try:
        return value.strftime("%b %d, %I:%M %p")
    except Exception:
        return str(value)




@app.route('/report')
def report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    db = get_db()
    cur = db.cursor(dictionary=True)

    params = []
    where = ''
    if start_date and end_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
        except Exception:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        try:
            end_dt = datetime.fromisoformat(end_date)
        except Exception:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        end_dt = end_dt + timedelta(hours=23, minutes=59, seconds=59)
        where = 'WHERE e.start_time >= %s AND e.end_time <= %s'
        params = [start_dt, end_dt]

    query = f"""
        SELECT e.event_id, e.title, e.start_time, e.end_time, r.resource_id, r.resource_name, r.resource_type
        FROM EventResourceAllocation a
        JOIN Event e ON a.event_id = e.event_id
        JOIN Resource r ON a.resource_id = r.resource_id
        {where}
        ORDER BY e.start_time ASC
    """

    if not (start_date and end_date):
        return render_template('report.html', resources_usage=None, start_date=None, end_date=None)

    cur.execute(query, params)
    rows = cur.fetchall()

    resources_usage = {}
    for r in rows:
        rid = r['resource_id']
        ev_start = r['start_time']
        ev_end = r['end_time']
        overlap_start = max(ev_start, start_dt)
        overlap_end = min(ev_end, end_dt)
        hours = 0.0
        if overlap_end and overlap_start and overlap_end > overlap_start:
            hours = (overlap_end - overlap_start).total_seconds() / 3600.0

        if rid not in resources_usage:
            resources_usage[rid] = {
                'resource_name': r['resource_name'],
                'resource_type': r['resource_type'],
                'total_hours': 0.0,
                'upcoming_bookings': []
            }
        resources_usage[rid]['total_hours'] += hours
        if r.get('title'):
            resources_usage[rid]['upcoming_bookings'].append(r['title'])

    resources_usage_list = []
    for v in resources_usage.values():
        v['upcoming_bookings'] = '; '.join(v['upcoming_bookings'])
        resources_usage_list.append(v)

    return render_template('report.html', resources_usage=resources_usage_list, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    app.run(debug=True)