import os
import os.path
import sys
import sqlite3
import unicodedata
from PyQt4 import QtCore, QtGui, QtSql, uic
from billQdialog import Bill_Dialog
from itertools import cycle
from functools import partial
# from kiwi_UI import Ui_MainWindow

# GLOBAL VAR
DB = "kiwiDB.db"
STYLES = ['blank.css', 'blender.css', 'blender_mod_btns.css']
# 'dark-blue.css', 'dark-green.css','dark-orange.css',
# 'light-blue.css', 'light-green.css','light-orange.css']
STYLE = cycle(STYLES)
STRING_CC = ""

# TODO LIST:
#  max line 1748
# ------------
# MAIN WINDOW:
#
# JOBS SUB-WINDOW:
# -create jobsTable DB and connect it to a model
# -add buttons in QT Designer for:
# -create btnNewJ and connect new_job() to display Vbox of mulitple QLineEdit
# -create btnEditB and connect edit_brief() to display Vbox of single QTextEdit
# -create btnModif and connect to modifications() to display a window w/
#                                   QLineEdit , Checkbox and 2 btns add and del
#
# BILLS SUB-WINDOW:
# -create billsTable DB and connect it to a model
# -add buttons in QT Designer for:
# create bill in database
# add Checkbox for ".pdf" ".docx" "Print"
# add button mail to
# ------------


class MyWindow(QtGui.QMainWindow):
    """Main class in which the app runs.

    A bit hacky but it is a running application, so lets focus on getting
    most things working, then we will think about updating the whole
    structure so that it makes more sense.
    Notes and abbreviations:
    WF      Wrapper function

    """

    def __init__(self, model, model2, model3):
        """Init taking all models of app. add more arguments for more models.

        At present time we take in 3 models used for the tableviews
        """
        super(MyWindow, self).__init__()
        # self.setupUi(self)

        def del_selected_jobs():
            """WF for jobs data using function `del_selected()`."""
            del_selected(self.jobsTable, model2,table="job")

        def del_selected_clients():
            """WF for clients data using function `del_selected()`."""
            del_selected(self.clientsTable, model)

        def combo_jobs_status():
            """Func to disable jobs btns unless sth selected in ComboBox."""
            print self.comboBoxClients.currentText()
            if "<Select Client>" in self.comboBoxClients.currentText():
                self.btnNewJ.setEnabled(False)
                self.btnEditBrief.setEnabled(False)
                self.btnDelJ.setEnabled(False)
            else:
                self.btnNewJ.setEnabled(True)
                self.btnEditBrief.setEnabled(True)
                self.btnDelJ.setEnabled(True)

        def update_combo_client_for_jobs():
            """Function update contents of ComboBox.

            Maybe needs to be rewritten to take following arguments:
            `ComboBox`, `ColumnName`, `Table` in order to fill ComboBox
            with rows from `ColumnName` in `Table`. To be addressed
            """
            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # print "\n"
            # print "-" * 80
            # print "START OF FUNCTION update combo client"
            # # UNCOMMENT SECTION FOR DEBUGGING /END/

            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # cursor.execute("""SELECT * FROM client""")
            # result_all = cursor.fetchall()
            # print "result all:", result_all
            # # UNCOMMENT SECTION FOR DEBUGGING /END/

            cursor.execute("""SELECT DISTINCT "Code_Client" FROM client""")
            result_key = cursor.fetchall()
            connection.close()

            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # print "result_key:", result_key
            # # UNCOMMENT SECTION FOR DEBUGGING /END/

            for p in result_key:
                p = list(p)
                if p[0] is not None:
                    # # UNCOMMENT SECTION FOR DEBUGGING /START/
                    # print "unecoded", p
                    # # UNCOMMENT SECTION FOR DEBUGGING /END/

                    p = unicodedata.normalize('NFKD',
                                              p[0]).encode('ascii', 'ignore')
                    # # UNCOMMENT SECTION FOR DEBUGGING /START/
                    # print "encoded" , p
                    # # UNCOMMENT SECTION FOR DEBUGGING /END/
                else:
                    # # UNCOMMENT SECTION FOR DEBUGGING /START/
                    # print p, "DID NOT ENCODE"
                    # # UNCOMMENT SECTION FOR DEBUGGING /END/
                    return
                for i in range(self.comboBoxClients.count()):

                    # # retrieve combox current items
                    allitems = [str(self.comboBoxClients.itemText(u))
                                for u in range(self.comboBoxClients.count())]
                    # # UNCOMMENT SECTION FOR DEBUGGING /START/
                    # print "All items:", allitems
                    # # UNCOMMENT SECTION FOR DEBUGGING /END/

                    if p not in allitems:
                        # # UNCOMMENT SECTION FOR DEBUGGING /START/
                        # print "DID NOT ADD ITEM TO COMBO BOX"
                        # # add the name of the client by list compreh. search
                        # tup = [item for item in result_all if p in item]
                        # print "code:", tup
                        # # UNCOMMENT SECTION FOR DEBUGGING /END/
                        self.comboBoxClients.addItem(p)
                        # # UNCOMMENT SECTION FOR DEBUGGING /START/
                        # print "ADDED ITEM %s TO COMBO BOX" % p
                        # print "All items:", allitems
                        # # UNCOMMENT SECTION FOR DEBUGGING /END/

            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # print "END OF FUNCTION update combo client"
            # print "-" * 80
            # print "\n"
            # # UNCOMMENT SECTION FOR DEBUGGING /END/

        def get_jobs_wrapper():
            """WF for jobs using function `get_jobs()`.

            Passed args are:
            self.comboBoxClients, self.jobsTable, self.model2
            """
            get_jobs(self.comboBoxClients, self.jobsTable, self.model2)

        def new_job_input_wrapper():
            """WF for jobs using function `new_job_input_dialog()`.

            To be replaced by a call to `input_window()`.
            Passed args are:
            self.comboBoxClients, self.jobsTable
            """
            new_job_input_dialog(self.comboBoxClients, self.jobsTable)

        def dock_toggle():
            """Func to toggle `Modifications` dock."""
            if self.dockWidget.isVisible() is True:
                self.dockWidget.close()
            else:
                self.dockWidget.show()

        def change_theme():
            """Func to change loaded Qt StyleSheet from menu."""
            global STYLE
            css = QtCore.QFile(os.path.join('themes', STYLE.next()))
            css.open(QtCore.QIODevice.ReadOnly)

            if css.isOpen():
                self.setStyleSheet(QtCore.QVariant(css.readAll()).toString())
            css.close()

        def new_client():
            """WF for `input_window()` to create new client.

            Passed args are:
            tab='client', fields=info2grab, mode='new',
            model=model, tabview=self.clientsTable
            """
            cols_i = [0, 1, 2, 3, 4, 7]
            info2grab = ["Nom", "Societe", "Telephone", "Email"]
            input_window(tab='client', fields=info2grab,
                         mode='new', model=model,
                         tabview=self.clientsTable, cols_to_fetch=cols_i)

        def edit_client():
            """WF for `input_window()` to edit new client.

            Passed args are:
            tab='client', fields=info2grab, mode='edit',
            model=model, tabview=self.clientsTable
            """
            # cols index in tableview to fetch, 0=key, 2="Nom" etc...
            cols_i = [0, 1, 2, 3, 4, 7]
            # button names to create = column names in sqlite3
            info2grab = ["Nom", "Societe", "Telephone", "Email"]
            input_window(tab='client', fields=info2grab,
                         mode='edit', model=model,
                         tabview=self.clientsTable, cols_to_fetch=cols_i)

        def new_job():
            """WF for `input_window()` to create new job.

            Passed args are:
            tab='client', fields=info2grab, mode='new',
            model=model, tabview=self.clientsTable
            """
            cols_i = [0, 1, 2, 3, 4, 5, 6, 7]

            info2grab = ["Code_Job", "Produit", "Brief", "Date_Debut",
                         "Date_Fin", "Prix", "Somme_Payee"]
            input_window(tab='job', fields=info2grab,
                         mode='new', model=model2, combo=self.comboBoxClients,
                         tabview=self.jobsTable, cols_to_fetch=cols_i)


        def edit_job():
            # cols_i = [0, 1, 2, 3, 4, 5, 6]
            cols_i = [0, 1, 2, 3, 4, 5, 6, 7]
            info2grab = ["Code_Job","Produit", "Brief", "Date_Debut",
                         "Date_Fin", "Prix", "Somme_Payee"]
            input_window(tab='job', fields=info2grab,
                         mode='edit', model=model2,
                         tabview=self.jobsTable, cols_to_fetch=cols_i)

        def new_bill_input_wrapper():
            """WF for bills using function `new_bill_input_dialog()`.

            Passed args are:
            self.comboBoxClients, self.billsTable
            """
            new_bill_input_dialog(self.comboBoxClients, self.billsTable)

        def getfiles(self):
            """Func to display window to retrieve file."""
            dlg = QtGui.QFileDialog()
            dlg.setFileMode(QtGui.QFileDialog.AnyFile)
            dlg.setFilter("SQLite file (*.db)")

            set_style(dlg)
            filenames = QtCore.QStringList()

            if dlg.exec_():

                filenames = dlg.selectedFiles()
                f = open(filenames[0], 'r')

                with f:
                    data = f.read()
                    self.contents.setText(data)

        # # Configure btns, views, models
        self.model = model
        self.model2 = model2
        self.model3 = model3

        # # load ui
        uic.loadUi('kiwi_UI.ui', self)

        # # load db into tableClients
        self.clientsTable.setModel(self.model)
        self.clientsTable.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)

        # close dock widget by default
        self.dockWidget.close()

        # trick to auto resize columns
        self.clientsTable.setVisible(False)
        self.clientsTable.resizeColumnsToContents()
        self.clientsTable.resizeRowsToContents()
        self.clientsTable.setVisible(True)

        self.clientsTable.setShowGrid(False)
        # self.clientsTable.horizontalHeader().setVisible(False)
        self.clientsTable.setSortingEnabled(True)

        init_tree_view(self.treeView)

        self.comboBoxClients.currentIndexChanged.connect(combo_jobs_status)
        self.comboBoxClients.highlighted.connect(update_combo_client_for_jobs)
        self.comboBoxClients.activated.connect(get_jobs_wrapper)

        self.actionCycle_Theme.triggered.connect(change_theme)
        self.actionLoad.triggered.connect(getfiles)

        # # diable job buttons if no clients selected
        self.btnNewJ.setEnabled(False)
        self.btnEditBrief.setEnabled(False)
        self.btnDelJ.setEnabled(False)
        self.btnNewBill.setEnabled(True)

        self.btnNewC.clicked.connect(new_client)
        self.btnEditC.clicked.connect(edit_client)
        self.btnNewJ.clicked.connect(new_job)
        self.btnEditBrief.clicked.connect(edit_job)
        self.btnNewBill.clicked.connect(new_bill_input_wrapper)

        self.btnDelC.clicked.connect(del_selected_clients)
        self.btnDelJ.clicked.connect(del_selected_jobs)
        self.btnModif.clicked.connect(dock_toggle)

        self.show()


class MyModel(QtSql.QSqlTableModel):
    """Load model for DB manipulation using forms and QTableview."""

    def __init__(self, parent=None, tab=None):
        """Instantiate `QtSql.QSqlTableModel` & select sqlite3 table `tab`.

        Args:
            tab (QtGui.QTableview): The table to SELECT using sql

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        super(MyModel, self).__init__(parent)
        self.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.setTable(tab)
        self.select()


def set_style(widget):
    """Func used to apply css styling to window. Uses global variables."""
    global STYLES
    global STYLE
    for i in range( (len(STYLES) - 1)):
        a = STYLE.next()

    css = QtCore.QFile(os.path.join('themes', STYLE.next()))
    css.open(QtCore.QIODevice.ReadOnly)
    if css.isOpen():
        widget.setStyleSheet(QtCore.QVariant(css.readAll()).toString())
    else:
        print "set_style() failed !"
    css.close()


def make_db():
    """Func used to create new SQlite DB for app usage.

    Should remove hardcoded data when done...
    """
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    # DB has three main tables and 2 linking tables.
    # Code copied and pasted 3 times... need to find sol, in te mean time it
    # works...

    # clients table ...
    cursor.execute("""
        CREATE TABLE client (
        "key" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Code_Client" VARCHAR(30),
        "Nom" VARCHAR(30),
        "Societe" VARCHAR(30),
        "Telephone" VARCHAR(30),
        "Factures_Payees" INTEGER(1),
        "Factures_Recues" INTEGER(1),
        "Email" VARCHAR(40),
        UNIQUE ("key") );""")

    # Populate db with some data ...
    cursor = connection.cursor()
    staff_data = [
        (55, "James", "kaloumba", "021 69 74 49", 5, 8, "ceemss.saiatgmail"),
        (7, "WilliamNOT", "sadoomba", "021 69 74 49", 5, 8, "cf.saiatgmail"),
        (7, "William", "badoomba", "021 69 74 49", 5, 8, "ceems.saiatgmail"),
        (7, "Williwas", "frambounda", "021 69 74 49", 5, 8, "ceemssatgmail")
    ]
    cursor.executemany("""
        INSERT INTO client ("key","Code_Client", "Nom", "Societe", "Telephone",
            "Factures_Payees", "Factures_Recues", "Email")
        VALUES(NULL,?,?,?,?,?,?,?)""", staff_data)
    connection.commit()

    # Fetch entire table of clients and store in `result_all`, and fetch
    # key data from first colmun `i[0]` in result_all through list compreh.
    # and store that  in result_cc (client code).
    # Could have used `SELECT key from client` but needded info for DEBUGGING
    #
    cursor.execute("""SELECT * FROM client""")
    result_all = cursor.fetchall()
    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # print "-" * 80
    # print "-" * 80
    # print("fetchall before cc update:")
    # for r in result_all:
    #     print(r)
    # # UNCOMMENT SECTION FOR DEBUGGING /END/

    result_cc = [i[0] for i in result_all]
    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # print "result_cc = ", result_cc
    # # UNCOMMENT SECTION FOR DEBUGGING /END/

    # Code below takes the unique key generated by SQL and appends `00` to it
    # to make it nicer looking when printing client numbers
    for i in result_cc:
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # print "i=", i
        # # UNCOMMENT SECTION FOR DEBUGGING /END/
        count = "00" + str(i)
        count = count[-3:]
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # print "concatenated:", count
        # # UNCOMMENT SECTION FOR DEBUGGING /END/
        cursor.execute("""
            UPDATE client SET "Code_Client" = SUBSTR('000'||%s,-3, 3)
            WHERE "key" = %d  """ % (count, i))
    connection.commit()

    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM client")
    # result_all = cursor.fetchall()
    # print "-" * 80
    # print("fetchall after cc update:")
    # for r in result_all:
    #     print(r)
    # print "-" * 80
    # print "-" * 80
    # # UNCOMMENT SECTION FOR DEBUGGING /END/

    # Jobs table ...
    cursor.execute("""
        CREATE TABLE job (
        "key" INTEGER PRIMARY KEY ,
        "Code_Job" VARCHAR(9),
        "Produit" TEXT,
        "Brief" VARCHAR(30),
        "Date_Debut" VARCHAR(10),
        "Date_Fin" VARCHAR(10),
        "Prix" VARCHAR(30),
        "Somme_Payee" VARCHAR(30),
        UNIQUE ("key"));""")

    job_data = [
        ("J-001-001", "client 1", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-001-002", "client 1", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-002-003", "client 2", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-002-004", "client 2", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-002-005", "client 2", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-003-006", "client 3x", "descri", "15-06-2015", "17-10-2017", 15, 5),
        ("J-003-007", "client 3x", "descri", "15-06-2015", "17-10-2017", 15, 5),
    ]
    cursor.executemany("""
        INSERT INTO job ("key", "Code_Job","Produit", "Brief", "Date_Debut",
                         "Date_Fin", "Prix", "Somme_Payee")
        VALUES(NULL,?,?,?,?,?,?,?)""", job_data)
    connection.commit()

    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # cursor.execute("SELECT * FROM job")
    # print("fetchall jobs:")
    # result = cursor.fetchall()
    # for r in result:
    #     print(r)
    # # UNCOMMENT SECTION FOR DEBUGGING /END/

    # "orders" table linking jobs to parent clients
    cursor.execute("""
        CREATE TABLE orders (
        key INTEGER PRIMARY KEY,
        client_id INTEGER,
        job_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES client(key),
        FOREIGN KEY(job_id) REFERENCES job(key)
        );""")

    order_data = [(1, 1),
                  (1, 2),
                  (2, 3),
                  (2, 4),
                  (2, 5),
                  (3, 6),
                  (3, 7),
                  ]
    cursor.executemany("""
        INSERT INTO orders ("key","client_id", "job_id")
        VALUES(NULL,?,?)""", order_data)
    connection.commit()

    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # cursor.execute("SELECT * FROM orders")
    # result_all = cursor.fetchall()
    # print "-" * 80
    # print("fetchall orders:")
    # for r in result_all:
    #     print(r)
    # print "-" * 80
    # # UNCOMMENT SECTION FOR DEBUGGING /END/

    # Bills table ...
    cursor.execute("""
        CREATE TABLE bill (
        "key" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Code_Facture" VARCHAR(9),
        "Produit" TEXT,
        "NAP" VARCHAR(30),
        "Date_Facture" VARCHAR(30),
        "Date_Paiement" VARCHAR(30),
        "Pourcentage_Paye" REAL,
        "Statut" VARCHAR(30),
        UNIQUE ("key","Code_Facture")
        );""")

    bill_data = [
        ("F-001-001", "bill description...", 15000,
            "15/06/2015", "17/10/2017", 50, "Publie"),
        ("F-002-002", "bill description...", 15000,
            "15/06/2015", "17/10/2017", 50, "Publie"),
        ("F-002-003", "bill description...", 15000,
            "15/06/2015", "17/10/2017", 50, "Publie"),
        ("F-003-004", "bill description...", 15000,
            "15/06/2015", "17/10/2017", 50, "Publie"),
        ("F-003-005", "bill description...", 15000,
            "15/06/2015", "17/10/2017", 50, "Publie"),
    ]
    cursor.executemany("""
        INSERT INTO bill ("key","Code_Facture", "Produit", "NAP",
            "Date_Facture", "Date_Paiement", "Pourcentage_Paye", "Statut" )
        VALUES(NULL,?,?,?,?,?,?,?)""", bill_data)
    connection.commit()

    # "confirmed" table linking bills to parent jobs and clients
    cursor.execute("""
        CREATE TABLE confirmed (
        key INTEGER PRIMARY KEY,
        client_id INTEGER,
        job_id INTEGER,
        bill_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES client(key),
        FOREIGN KEY(job_id) REFERENCES job(key)
        FOREIGN KEY(bill_id) REFERENCES bill(key)
        );""")

    confirmed_data = [(1, 1, 1),
                      (1, 2, 0),
                      (2, 3, 2),
                      (2, 4, 3),
                      (2, 5, 0),
                      (3, 6, 4),
                      (3, 7, 5),
                      ]

    cursor.executemany("""
        INSERT INTO confirmed ("key","client_id", "job_id", "bill_id")
        VALUES(NULL,?,?,?)""", confirmed_data)
    connection.commit()
    connection.close()


def del_selected(tabview, model, table=None ):
    """Func to diplay QtGui.QMessageBox before deleting entry.

    Args:
        table (QtGui.QTableview): The first parameter.
        param2 (QtSql.QSqlTableModel): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Warning)
    msg.setText("Are you sure you want to delete this data ?")
    # msg.setInformativeText("To edit a client you must select a row.")
    msg.setWindowTitle("Delete")
    msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    set_style(msg)
    result = msg.exec_()
    if result == QtGui.QMessageBox.Ok:
        if table == "job":
            # remove orders taoble sql and update
            L = tabview.selectionModel().selectedRows()
            for index in sorted(L):
                print('Row %d is selected' % index.row())

            index = tabview.selectedIndexes()[1]
            id_us = str(tabview.model().data(index).toString())
            print ("code : " + id_us)
        print 'Yes.'
        cid = str(id_us[4])
        jid = str(id_us[8])
        print "cid: ", cid
        print "jid: ", jid
        # Delete link from orders table
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        # id_us =  "\"" + id_us + "\""
        # cursor.execute("DELETE FROM orders WHERE Code_Job = '%s';" % id_us.strip())
        cursor.execute("""DELETE FROM orders
                          WHERE "client_id" = '%s' AND "job_id" = '%s' """ % (cid, jid))
        connection.commit()
        cursor.execute("""SELECT * FROM orders""")
        result_orders = cursor.fetchall()
        connection.close()
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        print "result orders after deletion:"
        for r in result_orders:
            print r


        indices = tabview.selectionModel().selectedRows()
        for index in sorted(indices):
            model.removeRow(index.row())
        lambda: model.removeRow(
            tabview.currentIndex().row())


    else:
        print 'No.'
    # warn.exec_()
    # w.close()


def input_window(tab=None, model=None, combo=None, cols_to_fetch=None,
                 fields=None, tabview=None, mode=None):
    """Create modal dialog w/ len(fields) rows of QPushButton & QLineEdit pairs.

    Args:
        tab (SQLITE table):  table to read/write.
        model (QtSql.QSqlTableModel): tableview model to update.
        combo (Qt.QtGui.QComboBox): combo box data to be fetched.
        fields (list):  List of strings to generate buttons. Strings must match
                        column names in SQL table
        mode (str): new mode or edit mode for SQLITE scripts
                    --if edit mode selected, we will display data to be
                    modified in QLineEdit. If undefined or new, it will
                    show empty... maybe redundant
    Returns:
        bool: The return value. True for success, False otherwise.
    """
    def get_text_input(var=None):
        text, ok = QtGui.QInputDialog.getText(
            var, 'Text Input Dialog', 'Enter Information:')
        if ok:
            var.setText(str(text))

    def get_text_input(var=None):

        text, ok = QtGui.QInputDialog.getText(
            var, 'Text Input Dialog', 'Enter Information:')

        if ok:
            var.setText(str(text))

    def cancel():
        win.close()

    def update_db_wrapper():
        col_dict = {}
        for key in fields:

            # print "lines[key].text():", lines[key].text()
            if key == "Code_Client" or key == "Code_Job" :
                print "key is BAD: ", key
                continue
            elif str(lines[key].text()):
                print "key is GOOD: ", key

                col_dict[key] = str(lines[key].text())
            else:
                return

        print "\n dict passed to update_db: "
        print col_dict
        print "row passed to update_db: ", key2read

        update_db(table=tab, row=key2read,
                  d=col_dict, close_win=win)
        model.select()

    def add_to_db_wrapper():
        #######################################################################
        # Part that updates DB entries
        #######################################################################
        col_dict = {}
        # print "Fields"
        # print fields


        for key in fields:
            # print "lines[key].text():", lines[key].text()
            if key == "Code_Client" or key == "Code_Job" :
                # print "key is BAD: ", key
                continue
            elif str(lines[key].text()):
                # print "key is GOOD: ", key

                col_dict[key] = str(lines[key].text())
            else:
                return
        if tab == "client":
            # add stuff here if client
            col_dict["Factures_Payees"] = 0
            col_dict["Factures_Recues"] = 0
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # print "dict passed to add_to_db_v2: "
        # print col_dict
        # # UNCOMMENT SECTION FOR DEBUGGING /END/
        add_to_db_v2(table=tab, d=col_dict, close_win=win)
        #######################################################################

        #######################################################################
        # Part that updates cc number live
        #######################################################################
        # UPDATE CLIENT CODE
        #####################
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM client""")
        result_all_clients = cursor.fetchall()
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # print "-" * 80
        # print "-" * 80
        # print("fetchall before cc update:")
        # for r in result_all_clients:
        #     print(r)
        # # UNCOMMENT SECTION FOR DEBUGGING /END/
        result_cc = [i[0] for i in result_all_clients]
        # print "result_cc = ", result_cc
        result_str = range(len(result_cc))
        int_str_tuple = result_str
        # print "result_str", result_str

        for idx, val in enumerate(result_cc):
            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # print "idx=", idx
            # # UNCOMMENT SECTION FOR DEBUGGING /END/
            count = "00000000" + str(val)  # +"\'"
            count = count[-3:]

            # count = "\"" + count + "\""
            # print "concatenated:", count
            result_str[idx] = count
            int_str_tuple[idx] = (count, val)
        # print "result_str", result_str
        if tab == "client":
            cursor.executemany("""
                UPDATE client SET "Code_Client" = ?
                WHERE "key" = ?""", int_str_tuple)
            # end of update cc
            connection.commit()
            connection.close()
        ########################################################################


        elif tab == "job":
            ####################################################################
            # Create entry in table ORDERS to keep track of who ordered what.
            ####################################################################
            item = [str(combo.currentText())]
            # fetch last job column
            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            cursor.execute("""SELECT DISTINCT "key" FROM job""")
            result_key = cursor.fetchall()
            connection.close()
            # print "All jobs in NewJobIptDia: ", result_key
            last = max(result_key)
            last = last[0]
            print "last: ", last
            print "should insert in row last+1: ", last + 1
            print "item[0]= ", item[0]

            # set values in dict
            m = "<Select Client>"
            orders_dict = {"key": "NULL",
                           "client_id": item[0],
                           "job_id": last,
                           }
            if item != m:
                # call method to update db######################################
                add_to_db_v2(table="orders", d=orders_dict, close_win=win)
                ################################################################

                ################################################################
                # UPDATE JOB CODE AND ORDERS TABLE
                ################################################################
                # UPDATE JOB CODE
                #################
                item[0] = "00000000" + str(item[0])  # +"\'"
                item[0] = item[0][-3:]
                last = "00000000" + str(last)  # +"\'"
                last = last[-3:]
                code_job_str = "J-" + item[0] + "-" + last
                params = [code_job_str, last]
                print "params: ", params

                connection = sqlite3.connect(DB)
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE job SET "Code_Job" = ?
                    WHERE "key" = ?""", params)
                connection.commit()
                connection.close()

            tabview.model().select()





        else:
            raise NotImplementedError

# STOPPED HERE
            # cursor.execute("""SELECT * FROM job""")
            # result_all_jobs = cursor.fetchall()
            # for i in result_cc:
            #     # # UNCOMMENT SECTION FOR DEBUGGING /START/
            #     # print "i=", i
            #     # # UNCOMMENT SECTION FOR DEBUGGING /END/
            #     count = "00000000" + str(i)  # +"\'"
            #     count = count[-3:]
            #     count = "\"" + count + "\""
            #     # print "concatenated:", count
            #     cursor.execute("""
            #         UPDATE client SET "Code_Client" = {s}
            #         WHERE "key" = {k}""" .format(s=count, k=i))
            #     # end of update cc
            # connection.commit()

        connection.close()
        model.select()

    # dict "existing_data" maps current data in db to qline edits for show
    existing_data = {}
    code = "---not yet created---"
    text = "Code "
    what = "Something went wrong...."
    window_info = "Information Input Window"

    for k in cols_to_fetch:
        existing_data[k] = ""
    if mode == "edit":
        # for i in sorted(indexes):
            # print('Row %d is selected' % i.row())
            # print "col"
        try:
            L = tabview.selectionModel().selectedRows()
            for index in sorted(L):
                print('Row %d is selected' % index.row())
            # uncomment for debug, view number of columns in table
            # (stored in all_indices)
            # all_indices = len(tabview.selectedIndexes()[:])
            # print "ALL INDICES: ", all_indices

            # cols_to_fetch = [1, 2, 3, 4, 7]
            print cols_to_fetch
            for k in cols_to_fetch:
                # print "k:", k
                i = tabview.selectedIndexes()[k]
                existing_data[k] = str(tabview.model().data(i).toString())
                if (k == 0):
                    key2read = int(existing_data[k])

                    # key2read = "\'" + str(key2read) + "\'"
                    # print "key2read: ", key2read
                # print "Existing data: ", existing_data[k]
            # print existing_data

        except (IndexError, ValueError ):

            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)

            msg.setText("Oops! Selection Error:")
            msg.setInformativeText("To edit a client you must select a row.")
            msg.setWindowTitle("Input Error")

            msg.setStandardButtons(QtGui.QMessageBox.Ok |
                                   QtGui.QMessageBox.Cancel)
            set_style(msg)
            msg.exec_()
            return
        # small section to format window according to table being acessed
        if (tab == 'client'):
            code = "00" + str(existing_data[0])
            text += ' Client'
            what = ' Client'
            window_info = "Client Information Input Window"

        elif (tab == 'job') or (tab == 'bill'):
            code = str(existing_data[1])
            text += ' Job'
            what = 'Job'
            window_info = "Job Information Input Window"
        else:
            return

    win = QtGui.QDialog()
    layout = QtGui.QGridLayout()
    layout.setVerticalSpacing(5)
    layout.setHorizontalSpacing(5)
    label = QtGui.QLabel()
    label.setText(
        "Please enter information by clicking on the buttons on the right.")
    label.setSizePolicy(QtGui.QSizePolicy.Expanding,
                        QtGui.QSizePolicy.Preferred)
    label.setFont(QtGui.QFont('', 12))
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 2)
    if (tab == 'client'):
        cols_to_fetch = cols_to_fetch[1:]
        code = "---not yet created---"
        what = " Client"
        text += what

        window_info = "Information Input Window"
    elif (tab == 'job'):
        cols_to_fetch = cols_to_fetch[1:]
        code = "---not yet created---"
        what = " Job"
        text += what
    else:
        raise NotImplementedError
    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # for k in cols_to_fetch:
    #     existing_data[k] = ""

    print "cols_to_fetch: ",cols_to_fetch
    print "fields:", fields
    # # UNCOMMENT SECTION FOR DEBUGGING /END/
    input_map = dict(zip(fields, cols_to_fetch))
    print "input map", input_map
    buttons = {}
    lines = {}
    i = 2

    # create buttons
    for key in fields:
        if key != ("Code_Job" or "Code_Client"):
            buttons[key] = QtGui.QPushButton(key)
            db_data = existing_data[input_map[key]]
            lines[key] = QtGui.QLineEdit(db_data)
            lines[key].setReadOnly(True)
            buttons[key].clicked.connect(partial(get_text_input, var=lines[key]))
            # # UNCOMMENT SECTION FOR DEBUGGING /START/
            # print buttons[key]
            # print lines[key]
            # # UNCOMMENT SECTION FOR DEBUGGING /END/
            layout.addWidget(buttons[key], i, 0)
            layout.addWidget(lines[key], i, 1)
            i += 1
        else:
            continue

    label2 = QtGui.QLabel()
    label2.setText("{txt}: {cc}".format(txt=text, cc=code))
    label2.setFont(QtGui.QFont('', 12))
    label2.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label2, 1, 0, 1, 2)

    btnDone = QtGui.QPushButton("Add" + what)
    btnCancel = QtGui.QPushButton("Cancel Operation")
    btnBox = QtGui.QHBoxLayout()
    btnBox.addWidget(btnDone)
    btnBox.addWidget(btnCancel)
    layout.addItem(btnBox, i + 1, 1)

    btnCancel.clicked.connect(cancel)
    if mode == "edit":
        btnDone.clicked.connect(update_db_wrapper)
    else:
        btnDone.clicked.connect(add_to_db_wrapper)

    win.setLayout(layout)
    win.setWindowTitle(window_info)
    set_style(win)
    height = 80 + 50 * len(fields)
    win.setFixedHeight(height)
    # win.setFixedWidth(400)
    win.exec_()


def get_jobs(combo, table, model2):
    """Fetch data from ComboBox & display corresponding rows in QTableView.

    Thia function will show only jobs of selected client by hiding all other
    rows than the ones linked by `orders` table.
    """
    # get items from client db
    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    # print "\n"
    # print "-" * 80
    # print "START METHOD 'get_jobs'... \n"
    # # UNCOMMENT SECTION FOR DEBUGGING /END/
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM orders""")
    result_orders = cursor.fetchall()
    connection.close()
    # # UNCOMMENT SECTION FOR DEBUGGING /START/
    print "result orders:"
    for r in result_orders:
        print r
    # # UNCOMMENT SECTION FOR DEBUGGING /END/
    # cursor.execute("""SELECT DISTINCT "Code_Client" FROM client""")
    # result_key = cursor.fetchall()
    # for r in result_key:
    #     print "result:", r
    selected_item = [str(combo.currentText())]
    # print "selected_item[0]= ", selected_item[0]
    m = "<Select Client>"
    n = "<View All>"

    # print "Condition input != <Select Clients> evaluates:", selected_item[0] != m

    # code here to take p and fetch all row ids from
    # orders table to display relevant rows from jobs table
    # load db into tableJobs
    table.setModel(model2)
    table.setSortingEnabled(False)
    table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    # trick to auto resize columns
    table.setVisible(False)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setVisible(True)
    table.setShowGrid(False)
    # table.setSortingEnabled(True)
    table.model().layoutChanged.emit()
    count = model2.rowCount()
    # print "count: ", count
    # print "client selected:", selected_item[0]
    if selected_item[0] == m:
        for i in range(count):
            table.hideRow(i)

    elif selected_item[0] == n:
        for i in range(count):
            table.showRow(i)
    else:
        # Explained in words: For each i, v in a enumerated list of L
        # (that makes i the element's position in the enumerated list
        # and v the original tuple) check if the tuple's first element
        # is 53, if so, append the result of the code before'for' to a
        # newly created list, here: i. It could also be my_function(i, v)
        # or yet another list comprehension. Since your list of tuples only has
        # one tuple with 53 as first value, you will get a list with one elemt.
        tup2 = [i for i, v in enumerate(result_orders) if v[
            1] == int(selected_item[0])]
        # print "list of jobs keys linked to client :", tup2
        for i in range(count):
            table.hideRow(i)
        for i in tup2:
            table.showRow(i)
        table.model().layoutChanged.emit()
        # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # print "Client<", selected_item[0], ">selected"
        # print "END OF METHOD 'get_jobs'... \n"
        # print "-" * 80
        # print "\n"
        # # UNCOMMENT SECTION FOR DEBUGGING /END/



def new_job_input_dialog(combo, table):
    def gettextProduct():
        text, ok = QtGui.QInputDialog.getText(product2add,
                                              'Text Input Dialog', 'Enter Contact Name:')
        if ok:
            product2add.setText(str(text))

    def gettextMail():
        text, ok = QtGui.QInputDialog.getText(email2add,
                                              'Text Input Dialog', 'Enter Contact Email:')
        if ok:
            email2add.setText(str(text))

    def gettextSdate():
        text, ok = QtGui.QInputDialog.getText(Sdate2add,
                                              'Text Input Dialog', 'Enter Company Number:')
        if ok:
            Sdate2add.setText(str(text))

    def gettextFdate():
        text, ok = QtGui.QInputDialog.getText(Fdate2add,
                                              'Text Input Dialog', 'Enter Company Number:')
        if ok:
            Fdate2add.setText(str(text))

    def gettextBrief():
        text, ok = QtGui.QInputDialog.getText(brief2add,
                                              'Text Input Dialog', 'Enter Company Name:')
        if ok:
            brief2add.setText(str(text))

    def getPrice():
        num, ok = QtGui.QInputDialog.getInt(
            price2add, "integer input dualog", "enter a number", 0)

        if ok:
            price2add.setText(str(num))

    def getPaid():
        num, ok = QtGui.QInputDialog.getInt(
            paid2add, "integer input dualog", "enter a number", 0)

        if ok:
            paid2add.setText(str(num))

    def cancel():
        win.close()

    def update_db_wrapper():
        # ADD SOME CODE TO CREATE NEW ENTRY IN TABLE ORDERS
        # TO KEEP TRACK OF WHICH CLIENT ORDERED WHAT JOB
        # ALSO NEEDED WH SELECTING CLIENT TO SEE JOBS
        # OPTIONAL: ADD "SHOW ALL" CHECKBOX TO SHOW ALL JOBS
        # update values below
        col_dict = {"key": "NULL",
                    "Produit": str(product2add.text()),
                    "Brief": str(brief2add.text()),
                    "Date_Debut": str(Sdate2add.text()),
                    "Date_Fin": str(Fdate2add.text()),
                    "Prix": str(price2add.text()),
                    "Somme_Payee": str(paid2add.text()),
                    }

        test_dict = {
            "key": "NULL",
            "Produit": "Shooting",
            "Brief": "Pub Pepsi",
            'Date_Debut': "15/11/2016",
            'Date_Fin': "15/12/2016",
            "Prix": "2500000",
            "Somme_Payee": "1250000",
        }

        add_to_db_v2(table="job", d=col_dict, close_win=win)

        # create entry in link table ORDERS to keep track of who ordered what
        item = [str(combo.currentText())]

        # fetch last job column
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT "key" FROM job""")
        result_key = cursor.fetchall()
        connection.close()
        print "All jobs in NewJobIptDia: ", result_key
        last = max(result_key)
        last = last[0]
        print "last: ", last
        print "should insert in row last+1: ", last + 1
        print "item[0]= ", item[0]

        # set values in dict
        m = "<Select Client>"
        orders_dict = {"key": "NULL",
                       "client_id": item[0],
                       "job_id": last,
                       }
        if item != m:
            # call method to update db
            add_to_db_v2(table="orders", d=orders_dict, close_win=win)
        table.model().select()

    win = QtGui.QDialog()
    flo = QtGui.QFormLayout()
    flo.setVerticalSpacing(6)

    btn = QtGui.QPushButton("Produit")
    product2add = QtGui.QLineEdit()
    product2add.setReadOnly(True)
    btn.clicked.connect(gettextProduct)
    flo.addRow(btn, product2add)

    # convert this one to textedit not line edit
    btn1 = QtGui.QPushButton("Brief")
    brief2add = QtGui.QLineEdit()
    brief2add.setReadOnly(True)
    btn1.clicked.connect(gettextBrief)
    flo.addRow(btn1, brief2add)

    # convert this to date input , and duplicate for end date
    btn2 = QtGui.QPushButton("Date_debut")
    Sdate2add = QtGui.QLineEdit()
    Sdate2add.setReadOnly(True)
    btn2.clicked.connect(gettextSdate)
    flo.addRow(btn2, Sdate2add)

    # convert to int only and duplicate
    btn3 = QtGui.QPushButton("Date_Fin")
    Fdate2add = QtGui.QLineEdit()
    Fdate2add.setReadOnly(True)
    btn3.clicked.connect(gettextFdate)
    flo.addRow(btn3, Fdate2add)

    # convert to int only and duplicate
    btn4 = QtGui.QPushButton("Prix")
    price2add = QtGui.QLineEdit()
    price2add.setReadOnly(True)
    btn4.clicked.connect(getPrice)
    flo.addRow(btn4, price2add)

    # convert to int only and duplicate
    btn5 = QtGui.QPushButton("Somme_Payee")
    paid2add = QtGui.QLineEdit()
    paid2add.setReadOnly(True)
    btn5.clicked.connect(getPaid)
    flo.addRow(btn5, paid2add)

    btnDone = QtGui.QPushButton("Add to Jobs")
    btnCancel = QtGui.QPushButton("Cancel")

    layout = QtGui.QGridLayout()
    layout.addItem(flo, 1, 1)

    btnBox = QtGui.QHBoxLayout()
    btnBox.addWidget(btnDone)
    btnBox.addWidget(btnCancel)

    layout.addItem(btnBox, 2, 1)

    win.setLayout(layout)
    win.setGeometry(400, 200, 400, 200)
    win.setFixedHeight(250)
    win.setWindowTitle("Add New Job")
    win.show()

    btnDone.clicked.connect(update_db_wrapper)
    btnCancel.clicked.connect(cancel)


def new_bill_input_dialog(combo, table):

    def cancel():
        win.close()

    def update_db_wrapper():

        cursor.execute("""
            CREATE TABLE confirmed (
            key INTEGER PRIMARY KEY,
            client_id INTEGER,
            job_id INTEGER,
            bill_id INTEGER,
            FOREIGN KEY(client_id) REFERENCES client(key),
            FOREIGN KEY(job_id) REFERENCES job(key)
            FOREIGN KEY(bill_id) REFERENCES bill(key)
            );""")

        bill_dict = {
            "key": "NULL",
            "Produit": "Shooting",
            "Brief": "Pub Pepsi",
            'Date_Debut': "15/11/2016",
            'Date_Fin': "15/12/2016",
            "Prix": "2500000",
            "Somme_Payee": "1250000",
        }

        add_to_db_v2(table="bill", d=bill_dict, close_win=win)

        # create entry in link table ORDERS to keep track of who ordered what
        item = [str(combo.currentText())]

        # fetch last job column
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT "key" FROM job""")
        result_key = cursor.fetchall()
        connection.close()
        print "All jobs in NewJobIptDia: ", result_key
        last = max(result_key)
        last = last[0]
        print "last: ", last
        print "should insert in row last+1: ", last + 1
        print "item[0]= ", item[0]

        # set values in dict
        m = "<Select Client>"
        bill_dict = {"key": "NULL",
                     "client_id": item[0],
                     "job_id": last,
                     }
        if item != m:
            # call method to update db
            add_to_db_v2(table="orders", d=orders_dict, close_win=win)
        table.model().select()

    try:
        _fromUtf8 = QtCore.QString.fromUtf8
    except AttributeError:
        def _fromUtf8(s):
            return s

    try:
        _encoding = QtGui.QApplication.UnicodeUTF8

        def _translate(context, text, disambig):
            return QtGui.QApplication.translate(context, text, disambig, _encoding)
    except AttributeError:
        def _translate(context, text, disambig):
            return QtGui.QApplication.translate(context, text, disambig)

    win = Bill_Dialog()
    dialog = QtGui.QDialog()
    win.setupUi(dialog)


    set_style(dialog)
    dialog.exec_()

    # btnDone.clicked.connect(update_db_wrapper)
    # btnCancel.clicked.connect(cancel)


def init_tree_view(treeView):
    def addItems(parent, elements):

        for text, children in elements:
            item = QtGui.QStandardItem(text)
            parent.appendRow(item)
            if children:
                addItems(item, children)

    def openMenu(position):

        indexes = treeView.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()

                level += 1

        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(("Edit person"))
        elif level == 1:
            menu.addAction(("Edit object/container"))
        elif level == 2:
            menu.addAction(("Edit object"))

        menu.exec_(treeView.viewport().mapToGlobal(position))
    # data must be in te form:
    # https://wiki.python.org/moin/PyQt/Creating%20a%20context%20menu%20for%20a%20tree%20view

    data = [
        ("Alice", [
            ("Keys", []),
            ("Purse", [
                ("Cellphone", [])
            ])
        ]),
        ("Bob", [
            ("Wallet", [
                ("Credit card", []),
                ("Money", [])
            ])
        ])
    ]
    model = QtGui.QStandardItemModel()

    addItems(model, data)
    treeView.setModel(model)
    model.setHorizontalHeaderLabels([("Clients/Jobs/Factures")])
    treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


def add_to_db_v2(close_win=None, d=None, table=None):
    print "-" * 80
    print "START OF METHOD ADD TO DB V2:"

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    # tup = [item for item in d if "NULL" in d[item]]
    # print "check if there is a null: ", d[tup[0]]
    if table == "orders":
        cursor.execute("""INSERT INTO {tn} ("key") VALUES (NULL)""".
                       format(tn=table))
    else:
        cursor.execute("""INSERT INTO {tn} ("key") VALUES (NULL)""".
                       format(tn=table))
    print "Created new row for table"

    cursor.execute("""SELECT DISTINCT "key" FROM {tab}""".format(tab=table))
    result_key = cursor.fetchall()

    last = max(result_key)
    last = last[0]
    print "last key: ", last, "from table:", table
    print "should insert in row last+1: ", last + 1

    if (table and d) is not None:
        print "DATA TO ADD: ", d
        print "\n"
        print "METHOD 'add_to_db_v2' ADDING TO:"
        print "Table:", table
        print "\n"

        for k in d:

            print "Column: ", k
            print "Data:", d[k]

            if d[k] == "NULL":
                print "Truth test:", d[k] == "NULL"
                print "values is:", d[k], "(supposed to be NULL)"
                continue

            else:

                d[k] = "\"" + str(d[k]) + "\""

                print "normal value: ", d[k]
                cursor.execute("""UPDATE {tn} SET {col} = {data} WHERE key = {r}""".
                               format(tn=table, col=k, data=d[k], r=last))
                print "Added in col:", k, "value :", d[k]

            print "\n"

    else:
        print "Did not create", table
    print "last row id:", cursor.lastrowid
    connection.commit()
    model.select()
    connection.close()
    print "Finished add_to_db(args)"
    close_win.close()

    print "ENDOF OF METHOD ADD TO DB V2:"
    print "-" * 80


def update_db(close_win=None, d=None, table=None, row=None):

    print "\nEntered update_db(): ----------------------"
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    if (table and row and d) is not None:
        print "\n"
        print "dictionary: ", d
        print "\n"

        print "table:", table
        print "row: ", row
        for k in d:
            print "\n"

            print "col:", k, "type:", type(k)
            print "data:", d[k], "type:", type(d[k])

            d[k] = "'" + d[k] + "'"

            print "\n"

            cursor.execute("""UPDATE {tn} SET {col} = {data} WHERE key = {r}""".format(
                tn=table, col=k, data=d[k], r=row))
        connection.commit()
        connection.close()

    else:
        print " need a table, a row number and a dictonary of columns and data !"

    # cursor.execute("SELECT * FROM client")
    # result_all = cursor.fetchall()
    # print "-" * 80
    # print "-" * 80
    # print("fetchall before cc update:")
    # for r in result_all:
    #     print(r)
    # result_cc = [i[0] for i in result_all]
    # print "result_cc = ", result_cc
    # for i in result_cc:
    #     print "i=", i
    #     count = "00000000" + str(i)  # +"\'"
    #     count = count[-3:]

    #     # count = "'" + count + "'"
    #     print "concatenated:", count

    #     cursor.execute(
    #         """UPDATE client SET 'Code_Client' = {s} WHERE 'key' = {k}""" .format(s=count, k=i))

    # connection.commit()
    # cursor.execute("SELECT * FROM client")
    # result_all = cursor.fetchall()
    # print "-" * 80
    # print "-" * 80
    # print("fetchall after cc update:")
    # for r in result_all:
    #     print(r)


    close_win.close()
    print "\nExited update_db(): ----------------------"


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")

    if not os.path.exists(DB):
        make_db()

    myDb = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    myDb.setDatabaseName(DB)

    if not myDb.open():
        print "Unable to create connection!"
        sys.exit(1)

    model = MyModel(tab='client')
    model2 = MyModel(tab='job')
    model3 = MyModel(tab='bill')
    # app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

    window = MyWindow(model, model2, model3)

    sys.exit(app.exec_())
