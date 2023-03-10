from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from dga import db, auth
from collections import OrderedDict
import time
from .firebaseConfig import firebase
from .auth_utils import login_required
from .dga_utils import dt1, dt4, dt5, pentagon1, pentagon2


rtdatabase = Blueprint('rtdatabase', __name__)

@rtdatabase.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    try:
        user = auth.get_account_info(session['idToken'])['users'][0]
        
        if request.method == 'POST':
            if request.form['action'] == 'record':
                print(request.form)
                if add_record(user):
                    flash('Record name already exists', 'error')
                    return render_template("home.html")
                else:
                    flash('Record added successfully', 'msg')
                    return redirect(url_for('rtdatabase.home'))
                
                # print(get_last_record())
            else:
                ordered_dict = get_record(user, None)
                print(ordered_dict)
                record_name = next(iter(ordered_dict.keys())) # type: ignore
                record_query = next(iter(ordered_dict.values())) # type: ignore
                print(type(record_query))
                
                hydrogen = int(record_query['hydrogen'])
                methane = int(record_query['methane'])
                acetylene = int(record_query['acetylene'])
                ethylene = int(record_query['ethylene'])
                ethane = int(record_query['ethane'])
                cmonoxide = int(record_query['cmonoxide'])
                cdioxide = int(record_query['cdioxide'])
                
                img = None
                fault_type = None
                selected_val = None
                if request.form['action'] == 'triangle1':
                    img = 1
                    fault_type = dt1(ethylene, methane, acetylene)
                    selected_val = 'triangle1'
                elif request.form['action'] == 'triangle4':
                    img = 2
                    fault_type = dt4(methane, hydrogen, ethane)
                    selected_val = 'triangle4'
                elif request.form['action'] == 'triangle5':
                    img = 3
                    fault_type = dt5(ethylene, methane, ethane)
                    selected_val = 'triangle5'
                elif request.form['action'] == 'pentagon1':
                    img = 4
                    fault_type = pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
                    selected_val = 'pentagon1'
                elif request.form['action'] == 'pentagon2':
                    img = 5
                    fault_type = pentagon2(ethane, hydrogen, acetylene, ethylene, methane)
                    selected_val = 'pentagon2'
                    
                return render_template(
                    "home.html", img = img, fault = fault_type, record_name = record_name, selected_val = selected_val)

        return render_template("home.html")
            
    except:
        flash('Session expired, please login again', 'error')
        return redirect(url_for('authentication.index'))
    

@rtdatabase.route("/records", methods=['GET', 'POST']) # type: ignore
@login_required
def records():
    try:
        user = auth.get_account_info(session['idToken'])['users'][0]
    except:
        flash('Session expired, please login again', 'error')
        return redirect(url_for('authentication.index'))
    
    keys_and_timestamps = display_records(user)
    record_selected = request.args.get('record_name', '')
    print("Record selected: " + record_selected)
    
    if request.method == 'POST':
        if request.form['action'] == 'delete':
            print("Delete button pressed")
            db.child('records').child(user['localId']).child(record_selected).remove()

            flash(record_selected + ' deleted successfully', 'msg')
            return redirect(url_for('rtdatabase.records'))
        
        else:
            if record_selected == '':
                flash('Please select a record', 'error')
                return render_template("records.html", kt = keys_and_timestamps)
            
            ordered_dict = get_record(user, record_selected)
            query_dict = dict(ordered_dict)
            print(query_dict)
            
            hydrogen = int(query_dict['hydrogen'])
            methane = int(query_dict['methane'])
            acetylene = int(query_dict['acetylene'])
            ethylene = int(query_dict['ethylene'])
            ethane = int(query_dict['ethane'])
            cmonoxide = int(query_dict['cmonoxide'])
            cdioxide = int(query_dict['cdioxide'])
            
            img = None
            fault_type = None
            selected_val = None
            if request.form['action'] == 'triangle1':
                img = 1
                fault_type = dt1(ethylene, methane, acetylene)
                selected_val = 'triangle1'
            elif request.form['action'] == 'triangle4':
                img = 2
                fault_type = dt4(methane, hydrogen, ethane)
                selected_val = 'triangle4'
            elif request.form['action'] == 'triangle5':
                img = 3
                fault_type = dt5(ethylene, methane, ethane)
                selected_val = 'triangle5'
            elif request.form['action'] == 'pentagon1':
                img = 4
                fault_type = pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
                selected_val = 'pentagon1'
            elif request.form['action'] == 'pentagon2':
                img = 5
                fault_type = pentagon2(ethane, hydrogen, acetylene, ethylene, methane)
                selected_val = 'pentagon2'
                
            return render_template(
                "records.html", img = img, fault = fault_type, selected_val = selected_val, kt = keys_and_timestamps, record_selected = record_selected)
        
    return render_template("records.html", kt = keys_and_timestamps, record_selected = record_selected)


def add_record(user):
    record = request.form.get('rname')
    hydrogen = request.form.get('hydrogenconc')
    methane = request.form.get('methaneconc')
    acetylene = request.form.get('acetyleneconc')
    ethylene = request.form.get('ethyleneconc')
    ethane = request.form.get('ethaneconc')
    cmonoxide = request.form.get('cmonoxideconc')
    cdioxide = request.form.get('cdioxideconc')
    total = request.form.get('totalcombustibles')
    
    data = {
        "timestamp": time.time(), # firebase.database.ServerValue.TIMESTAMP,
        "hydrogen": hydrogen,
        "methane": methane,
        "acetylene": acetylene,
        "ethylene": ethylene,
        "ethane": ethane,
        "cmonoxide": cmonoxide,
        "cdioxide": cdioxide,
        "total_combustibles": total
    }
    
    # doing ref like this does not work somehow, will instead refresh the path everytime it is called
    # ref = db.child('records').child(user['localId'])
    
    # if user (localId) doesn't exist
    if db.child('records').child(user['localId']).get().val() is None:
        db.child('records').child(user['localId']).set({record: data})
    # if record name already exists
    elif db.child('records').child(user['localId']).child(record).get().val():
        return True
    # if record name doesn't exist
    else:
        print("Success")
        db.child('records').child(user['localId']).child(record).set(data)


def get_record(user, key):
    record = None
    if key:
        record = db.child('records').child(user['localId']).child(key)
    else:
        record = db.child('records').child(user['localId']).order_by_child('timestamp').limit_to_last(1)
        
    return record.get().val()


def display_records(user):
    try:
        all_records = db.child('records').child(user['localId']).get()
        keys = [record.key() for record in all_records.each()] # type: ignore
        timestamps = [time.ctime(record.val()['timestamp']) for record in all_records.each()] # type: ignore

        keys_and_timestamps = dict(zip(keys, timestamps))
    except:
        keys_and_timestamps = {"No records found": ""}

    return keys_and_timestamps


# Note to self:
# There are 2 ways to pass data in url:
# 1. using query string where the data is passed in the url itself, with ? and & as delimiters
# and the data is passed as key=value pairs in url_for(), and then using request.args.get() to get the data
# 2. using name of <input> where the data is passed in the form of <variable> in the url and the function
# must take in the variable as a parameter