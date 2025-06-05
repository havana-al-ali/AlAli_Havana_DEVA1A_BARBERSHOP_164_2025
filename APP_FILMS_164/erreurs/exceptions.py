import sys
from flask import flash, render_template
from pymysql import IntegrityError
from APP_FILMS_164 import app


class Base(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message




class ErreurFichierSqlDump(Base):
    pass

class ErreurFichierEnvironnement(Base):
    pass

class ExceptionInitApp(Base):
    pass

class ErreurConnectionBD(Base):
    pass

class ErreurExtractNameBD(Base):
    pass

class MaBdErreurDoublon(IntegrityError):
    pass

class MonErreur(Base):
    pass

class MaBdErreurConnexion(Base):
    pass

class DatabaseException(Base):
    pass

class SqlException(DatabaseException):
    pass

class ExceptionClientsAfficher():
    pass
class ExceptionClientUpdateWtf():
    pass
class ExceptionClientsAjouterWtf():
    pass
class ExceptionClientDeleteWtf(Base):
    pass


class SqlSyntaxError(SqlException):
    pass

class ExceptionServicesAjouterWtf(Base):
    pass

class ExceptionServiceUpdateWtf(Base):
    pass

class ExceptionServiceDeleteWtf(Base):
    pass
class ExceptionEmployeAddWtf(Base):
    pass

class ExceptionEmployeUpdateWtf(Base):
    pass

class ExceptionEmployeDeleteWtf(Base):
    pass



# ... autres exceptions ...

@app.errorhandler(Exception)
def om_104_exception_handler(error):
    msg = f"Erreur : {error}"
    if error.args:
        msg += f" {error.args[0]}"
    flash(msg, "danger")
    a, b, c = sys.exc_info()
    flash(f"Erreur générale : {a} {b} {c}", "danger")
    return render_template("home.html"), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
