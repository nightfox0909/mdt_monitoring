from datetime import datetime
from flask import request
from sqlalchemy import or_
from flask import Response
import hashlib

from sqlalchemy.sql.expression import true

from app import db
from app.flask_api import bp
from app.models import Computer, Status, Skew
from auxilliary.g_sheets_update import update_sheets
import uuid
import json

@bp.route('/MDTMonitorEvent/PostEvent', methods=['GET', 'POST'])
def PostEvent():
    uid = request.args.get('uniqueID', None)
    stepName = request.args.get('stepName', None)
    message = request.args.get('message', None)
    st_now = request.args.get('currentStep', None)
    st_total = request.args.get('totalSteps', None)
    computerName = request.args.get('computerName', None)
    severity = request.args.get('severity', None)
    dartIP = request.args.get('dartIP', None)
    dartPort = request.args.get('dartPort', None)
    dartTicket = request.args.get('dartTicket', None)
    vmHost = request.args.get('vmHost', None)
    vmName = request.args.get('vmName', None)
    u2id = request.args.get('id', None)
    unq, macAddress = u2id.split(',')
    messageID = request.args.get('messageID', None)

    m = hashlib.md5()
    m.update(u2id.encode('utf-8'))
    sys_gen_id = str(uuid.UUID(m.hexdigest(), version=4))

    if not uid:
        c1 = Computer.query.filter(or_(Computer.sys_generated_uid == sys_gen_id, Computer.computerName == computerName)).first()
        
        if not c1:
            c1 = Computer( 
                    computerName = computerName,
                    sys_generated_uid = sys_gen_id,
                    macAddress = macAddress,
                    unq_id = unq,
                    dartIP = dartIP,
                    dartPort = dartPort,
                    dartTicket = dartTicket,
                    vmHost = vmHost,
                    vmName = vmName,
                    finalName = '',
                    windows_key = '',
                    lisc_status = 'invalid',
                    completed = False
            )
        else:
            c1.computerName = computerName
    else:
        c1 = Computer.query.filter_by(sys_generated_uid = uid).first()
        if computerName != c1.computerName and computerName != c1.finalName:
            c1.finalName = computerName
    c1.last_seen = datetime.utcnow()
    s1 = Status(
            author = c1,
            stepName = stepName,
            message = message,
            st_now = st_now,
            st_total = st_total,
            severity = severity,
            messageID = messageID
        )
    if message == 'LTI deployment completed successfully':
        c1.completed = True
        sk1 = Skew.query.filter_by(id = c1.skew_id).first()
        update_sheets(c1, sk1)
    db.session.add(s1)
    db.session.add(c1)
    db.session.commit()    
    return Response(
            f'<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">{c1.sys_generated_uid}</string>',
            status=200,
            mimetype='application/xml'
        )  

@bp.route('/MDTMonitorEvent/GetSettings', methods=['GET'])
def GetSettings():
    uid = request.args.get('uniqueID', None)

    c1 = Computer.query.filter_by(sys_generated_uid = uid).first()
    c1.last_seen = datetime.utcnow()

    db.session.add(c1)
    db.session.commit()

    return Response(f'<Settings />', status=200, mimetype='text/xml')
    
@bp.route('/PostSpecs', methods=['POST'])
def PostSpecs():
    computerName = request.json.get('computerName', 'Dnage')
    c1 = Computer.query.filter(or_(Computer.finalName == computerName, Computer.computerName == computerName)).first()
    c1.windows_key = request.json.get('win_key', None)
    c1.lisc_status = request.json.get('lisc_status', None)
    c1.serial_number = request.json.get('serial', None)
    c1.asset_tag = request.json.get('asset_tag', None)
    c1.last_seen = datetime.utcnow()

    sk1 = Skew(
            ram_gb = request.json.get('ram', None),
            cpu = request.json.get('cpu', None),
            hdd_gb = request.json.get('hdd', None),
            system_family = request.json.get('sys_family', None),
            make = request.json.get('make', None),
            model = request.json.get('model', None),
            arch = request.json.get('arch', None),
            processor_count = request.json.get('proc_count', None),
            windows_version = request.json.get('win_ver', None)
        )

    sk2 = Skew.query.filter_by(md5_hash = sk1.get_hash()).first()
        
    if sk2:
        sk2.computers.append(c1)
        db.session.add(sk2)
    else:
        sk1.computers.append(c1)
        db.session.add(sk1)
        
    db.session.add(c1)
    db.session.commit()

    ret_code = {
                'status': 'ok',
                'op': 'new_add' if sk2 else 'updated'
                }
    return Response(json.dumps(ret_code),status=200,mimetype='application/json')

@bp.route('/InventoryUpdate', methods=['POST'])
def InventoryUpdate():
    uuid = request.args.get('id')
    state = request.args.get('state')
    