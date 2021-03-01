from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from hashlib import md5
from app import db

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    sys_generated_uid = db.Column(db.String(128), index=True, unique=True)
    macAddress = db.Column(db.String(128))
    unq_id = db.Column(db.String(128))
    dartIP = db.Column(db.String(32))
    dartPort = db.Column(db.String(32))
    dartTicket = db.Column(db.String(32))
    vmHost = db.Column(db.String(32))
    vmName = db.Column(db.String(32))
    computerName = db.Column(db.String(32))
    finalName = db.Column(db.String(32))
    windows_key = db.Column(db.String(128))
    lisc_status = db.Column(db.String(32))
    serial_number = db.Column(db.String(32))
    asset_tag = db.Column(db.String(32))
    skew_id = db.Column(db.Integer, db.ForeignKey('skew.id'))
    status_recieved = relationship("Status", backref="author", foreign_keys='Status.computer_id')#db.relationship("Status", backref='author', lazy='dynamic')


class Skew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ram_gb = db.Column(db.Integer)
    cpu = db.Column(db.String(64))
    hdd_gb = db.Column(db.Integer)
    system_family = db.Column(db.String(64))
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    arch = db.Column(db.String(32))
    processor_count = db.Column(db.Integer)
    windows_version = db.Column(db.String(64))
    md5_hash = db.Column(db.String(140))
    computers = db.relationship('Computer')

    def is_equal(self, sk2):
        if self.__class__ == sk2.__class__ and self.__dict__ == sk2.__dict__:
            return True
        else:
            return False
    
    def get_hash(self):
        sa = self.ram_gb +\
            self.cpu +\
            self.hdd_gb +\
            self.system_family +\
            self.make +\
            self.model +\
            self.arch +\
            self.processor_count +\
            self.windows_version
        self.md5_hash = md5(sa.encode('utf-8')).hexdigest()
        return self.md5_hash

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    stepName = db.Column(db.String(128))
    message = db.Column(db.String(140))
    st_now = db.Column(db.Integer)
    st_total = db.Column(db.Integer)
    severity = db.Column(db.Integer)
    messageID = db.Column(db.Integer)