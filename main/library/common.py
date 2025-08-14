import json
import uuid
import re
import io
import itertools
import jwt
import bcrypt
import random
from sqlalchemy.orm import Query, Session
from sqlalchemy import desc, case, func, DECIMAL
from datetime import datetime, date, timedelta as td
from fastapi import Response
from itertools import groupby
from main.core.config import Settings
from uuid import uuid4
from openpyxl import Workbook

settings = Settings()


class Common:

    def uuid_generator(self):

        return str(uuid.uuid4())

    def is_valid_uuid(self, value):
        try:
            uuid.UUID(value)

            return True
        except ValueError:
            return False

    def get_timestamp(self, wtime=0, datetime_fmt=0):

        if datetime_fmt:
            return (datetime.utcnow() + td(hours=8)).replace(microsecond=0)

        if wtime:
            timestamp = str(
                (datetime.utcnow() + td(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            )
        else:
            timestamp = str(
                (datetime.utcnow() + td(hours=8)).strftime("%Y-%m-%d")
            )

        return timestamp

    def read_json(self, _file):

        config = {}
        with open("%s.json" % _file, "r") as f:
            config = json.load(f)
        return config

    def key_remover(self, dictionary, keys):

        dictionary = dict(dictionary)
        dictionary = dictionary.copy()

        for key in keys:

            # DELETE KEY
            if key in dictionary:
                del dictionary[key]

        # RETURN FINAL DICTIONARY
        return dictionary

    def create_standard_obj(self, standard, doc):

        standard_obj = {}

        for stnrd in standard:
            standard_obj[stnrd] = doc[stnrd]

        return standard_obj

    def round_num(self, num=0, decimal=2, doc={}, keys=[]):

        try:
            if keys:
                for k in keys:
                    if not num:
                        num = (
                            float(doc[k])
                            if k in doc
                            and doc[k]
                            and doc[k] not in ["None", "NONE"]
                            else 0
                        )
            else:
                num = float(num) if num else 0
        except:
            pass

        num = round(num * (10**decimal), 3)
        num = round(round(num) / (10**decimal), decimal)

        return num

    def escape_sc(self, event, chars=[]):

        # array of find and replace pairs
        if not chars:
            chars = [("'", "''")]

        if not event:
            return event

        for c in chars:
            try:
                event = str(event).replace(c[0], c[1])
            except:
                event.replace(c[0], c[1])

        return event

    def remove_T_separator(self, docs):

        if not docs or (docs and type(docs) is not list):
            return []

        final_docs = []

        for doc in docs:

            doc_keys = list(doc.keys())

            for dockey in doc_keys:

                if "ed_at" in dockey or (
                    dockey == "date" and re.search(r"T", str(doc[dockey]))
                ):
                    datestring = str(doc[dockey])
                    doc[dockey] = datestring.replace("T", " ")

            final_docs.append(doc)

        return final_docs

    def format_csv(self, rawData):
        # FORMAT CSV
        header = rawData["header"]
        headers = (
            rawData["headers"]
            if "headers" in rawData and rawData["headers"]
            else ()
        )
        csvData = [",".join(headers if headers else header)]
        for x in rawData["rows"]:
            row = [
                (str(x[head]) if not "," in str(x[head]) else '"%s"' % x[head])
                if head in x and x[head] not in ([], {}, None, "None")
                else ""
                for head in header
            ]
            csvData.append(",".join(row))

        return "\n".join(csvData)

    def format_excel(self, rawData, is_raw_file=0):
        # FORMAT EXCEL
        wb = Workbook()
        ws = wb.active
        if rawData.get("sheet_name"):
            ws.title = rawData["sheet_name"]

        header = rawData["header"]
        headers = rawData["headers"] if rawData.get("headers") else ()
        ws.append(tuple(headers if headers else header))
        for x in rawData["rows"]:
            row = [
                x[h] if h in x and x[h] not in ["None"] else "" for h in header
            ]
            ws.append(tuple(row))

        for d in rawData["sheets"] if rawData.get("sheets") else []:
            _header = d["header"]
            _headers = d["headers"] if d.get("headers") else ()
            _ws = wb.create_sheet(d["sheet_name"])
            _ws.append(tuple(_headers if _headers else _header))

            for e in d["rows"]:
                _row = [
                    e[h] if h in e and e[h] not in ["None"] else ""
                    for h in _header
                ]
                _ws.append(tuple(_row))

        if is_raw_file:
            wb.save("tmp.xlsx")
        else:
            output = io.BytesIO()
            wb.save(output)
            data = output.getvalue()
            return data

    def get_media_return(self, file_name, file_type, data):
        # GET RETURN
        fileTypes = {
            "csv": "text/csv",
            "xls": "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        fname = f'"{file_name}.{file_type}"'
        headers = {
            "Content-Disposition": f"attachment; filename={fname}",
            "Content-Type": fileTypes[file_type],
        }
        return Response(
            data,
            headers=headers,
        )

    def clean_doc(self, doc):
        if "_id" in doc:
            doc["id"] = doc["_id"]
            del doc["_id"]
        if "_rev" in doc:
            doc["rev"] = doc["_rev"]
            del doc["_rev"]

        return doc

    def str_to_date(self, date_str: str, seperator: str):
        return datetime.strptime(date_str, f"%Y{seperator}%m{seperator}%d")

    def get_year(self):
        year = str((datetime.utcnow() + td(hours=8)).strftime("%Y"))
        return year

    def get_epoch_timestamp(self):
        timestamp = str((datetime.utcnow() + td(hours=8)).strftime("%s"))
        return timestamp

    def get_vector(self, *args):
        vector = list(map(lambda x: list(x), itertools.product(*args)))
        return vector

    def group_list_by_key(self, lst: list, key: str):
        group_func = lambda x: str(x.get(key))
        lst = sorted(lst, key=group_func)
        return groupby(lst, key=group_func)

    def get_cdb_values(self, docs, key):
        return list(map(lambda x: x.get(key), docs.get("rows", [])))

    def couch_db_sort(self, sort_field, sort_value, sort_type, is_list=False):

        if not (sort_field and sort_value):
            return None

        return (
            "%s%s<%s>"
            % (
                ("-" if sort_value == "desc" else "+"),
                sort_field,
                sort_type or "string",
            )
            if not is_list
            else [{sort_field: sort_value}]
        )

    def postgres_sort(self, Model, sort_field, sort_value):
        table_columns = Model.__table__.columns
        if sort_field in table_columns:
            sort = table_columns[sort_field]
            return sort.asc if sort_value == "asc" else sort.desc
        else:
            return Model.created_at.desc

    def sort_query(
        self, query: Query, sort_field="created_at", sort_value="asc"
    ):
        if not self.is_sort_field_valid(query, sort_field):
            return query

        return query.order_by(
            sort_field if sort_value == "asc" else desc(sort_field)
        )

    def batch(self, iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    def tupple_element_remover(self, tpl: tuple, key: any):
        tpl = list(tpl)
        if key in tpl:
            tpl.remove(key)
        return tuple(tpl)

    def validate_fields_from_model(
        self, table_model, doc: dict, no_invalid=True
    ):
        columns = table_model.__table__.columns.keys()
        for d in doc.keys():
            if not d in columns and not no_invalid:
                continue

            if not d in columns:
                return False, f"Invalid column '{d}'"

            if str(
                table_model.__table__.c[d].type
            ) == "UUID" and not self.is_valid_uuid(doc[d]):
                return False, f"Invalid ID value for '{d}'"

            _type = table_model.__table__.c[d].type.python_type
            if not isinstance(doc[d], _type):
                try:
                    _type(doc[d])
                except:
                    return (
                        False,
                        f"Invalid column type for '{d}',"
                        f" expected: '{_type.__name__}'",
                    )
                else:
                    continue

        return True, ""

    def get_offset(self, page: int = None, limit: int = None) -> int:
        return (page - 1) * limit if page and limit else None

    def generate_jwt(self, data):
        secret = settings.SECRET
        algorithm = settings.JWT_ALGO
        token = jwt.encode(data, secret, algorithm)
        return token

    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), 
            hashed_password.encode("utf-8")
        )

    def uuid_with_dash(self):
        uid = str(uuid4()).replace("-","")
        return uid

    def generate_temporary_password(self):
        su = self.uuid_with_dash()
        tmp = su[:8]
        return tmp

    def generate_hashed_password(
        self,
        password_str: str
    ):
        return bcrypt.hashpw(
            password_str.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def generate_ref_id(self):
        su = self.uuid_with_dash()
        otp = su[:6]
        return otp

    def generate_mobile_otp(self):
        return str(random.randint(1000, 9999))

    def normalize_ph_number(self, phone: str):
        phone = phone.strip()
        if phone.startswith("09"):
            return phone[1:]
        elif phone.startswith("+63"):
            return phone[3:]
        else:
            return None

    def small_letter_no_space(self, orig: str):
        return re.sub(r"\s+", "", orig.lower())
    

    def get_time_left_til_midnight(self):
        now = datetime.now()
        midnight = (now + td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_diff = int((midnight - now).total_seconds())
        return seconds_diff

common = Common()
