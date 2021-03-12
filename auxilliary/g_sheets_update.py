import requests
from config import Config
from app.decorators import async1
from app.models import Computer, Skew
import datetime

@async1
def update_sheets(c1: Computer, sk1: Skew):
    if not Config.ENABLE_SHEETS_UPDATE:
        return
    
    dt_t = datetime.datetime.today()
    params = {
        'entry.504710583': c1.sys_generated_uid,    #UID
        'entry.2047695267': sk1.make,               # Manufacturer
        'entry.1989428453': sk1.system_family,      # System family
        'entry.1683356396': sk1.model,              # Model
        'entry.1653489536': c1.serial_number,       # Serial
        'entry.311548602': sk1.cpu,                 # CPU
        'entry.2021143121': sk1.ram_gb,             # RAM
        'entry.1552576243': sk1.processor_count,    # Logical processors
        'entry.960514414': sk1.hdd_gb,              # HDD size
        'entry.1264821243': c1.windows_key,         # Windows Key
        'entry.1566079507_year': dt_t.year,
        'entry.1566079507_month': dt_t.month,
        'entry.1566079507_day': dt_t.day,
        'entry.213377782' : 'Provisioned',          # Status
        'entry.1827534865': sk1.arch,               # Arch
        'entry.901574010': sk1.windows_version,     # Windows model
        'entry.608745030': c1.lisc_status
    }
    requests.post(Config.SHEETS_BACKEND, params=params)

