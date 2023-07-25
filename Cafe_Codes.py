from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
import Cafe_Design
import random


class Cafe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cafe_win = Cafe_Design.Ui_winCafe()
        self.cafe_win.setupUi(self)

        self.cash = 397
        self.options = "🍔"

        self.serv_speed = 10
        self.shoes_fee = 400
        self.shoes_bought = False

        self.serv_x = 430
        self.serv_y = 330

        self.waiter_x = 430
        self.waiter_y = 330
        self.customer_x = -134

        self.order_details = dict()

        self.fetch_point_y = 744

        self.ready_y = 760

        self.hamb_fee = 3
        self.hamb_upgrade_fee = 3
        self.hamb_progress = 0
        self.hamb_level = 1

        self.open_frier_fee = 125
        self.fries_fee = 8
        self.fries_upgrade_fee = 18
        self.fries_progress = 0
        self.fries_level = 1

        self.open_oven_fee = 600
        self.pizza_fee = 50
        self.pizza_upgrade_fee = 70
        self.pizza_progress = 0
        self.pizza_level = 1

        self.cafe_win.lblThink.setHidden(True)
        self.cafe_win.lblOrder.setHidden(True)

        self.cafe_win.lblHambReady.setHidden(True)
        self.cafe_win.lblFriesReady.setHidden(True)
        self.cafe_win.lblPizzaReady.setHidden(True)

        self.cafe_win.frmUpgradeHamburgers.setHidden(True)
        self.cafe_win.frmUpgradeFries.setHidden(True)
        self.cafe_win.frmUpgradePizza.setHidden(True)

        self.cafe_win.lblFriesPic.setHidden(True)
        self.cafe_win.lblPizzaPic.setHidden(True)

        self.cafe_win.frmOpenFrier.setHidden(True)
        self.cafe_win.frmOpenOven.setHidden(True)

        self.cafe_win.btnStart.clicked.connect(self.new_customer)

        self.cafe_win.btnToaster.clicked.connect(lambda: self.upgrade_frame("hamburger", '', self.cafe_win.frmUpgradeHamburgers))
        self.cafe_win.btnUpgradeHamb.clicked.connect(lambda: self.upgrade(self.hamb_fee, self.hamb_upgrade_fee, self.hamb_level, self.hamb_progress, self.cafe_win.btnUpgradeHamb, self.cafe_win.lblHambFee, self.cafe_win.lblHambLevel, self.cafe_win.prgHambLevel, "hamb"))
        self.cafe_win.btnCloseHamb.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmUpgradeHamburgers))

        self.cafe_win.btnFrier.clicked.connect(lambda: self.upgrade_frame("fries", self.cafe_win.btnFrier, [self.cafe_win.frmOpenFrier, self.cafe_win.frmUpgradeFries]))
        self.cafe_win.btnUpgradeFries.clicked.connect(lambda: self.upgrade(self.fries_fee, self.fries_upgrade_fee, self.fries_level, self.fries_progress, self.cafe_win.btnUpgradeFries, self.cafe_win.lblFriesFee, self.cafe_win.lblFriesLevel, self.cafe_win.prgFriesLevel, "fries"))
        self.cafe_win.btnCloseFries.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmUpgradeFries))
        self.cafe_win.btnOpenFrier.clicked.connect(self.open_frier)
        self.cafe_win.btnCloseFrier.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmOpenFrier))

        self.cafe_win.btnOven.clicked.connect(lambda: self.upgrade_frame("pizza", self.cafe_win.btnOven, [self.cafe_win.frmOpenOven, self.cafe_win.frmUpgradePizza]))
        self.cafe_win.btnUpgradePizza.clicked.connect(lambda: self.upgrade(self.pizza_fee, self.pizza_upgrade_fee, self.pizza_level, self.pizza_progress, self.cafe_win.btnUpgradePizza, self.cafe_win.lblPizzaFee, self.cafe_win.lblPizzaLevel, self.cafe_win.prgPizzaLevel, "pizza"))
        self.cafe_win.btnClosePizza.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmUpgradePizza))
        self.cafe_win.btnOpenOven.clicked.connect(self.open_oven)
        self.cafe_win.btnCloseOven.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmOpenOven))

        self.cafe_win.btnBetterShoes.clicked.connect(self.shoes)

    def new_customer(self):
        self.cafe_win.btnStart.setHidden(True)
        self.customer_timer = QTimer()
        self.customer_timer.timeout.connect(self.customer_comes)
        self.customer_timer.start(4)

    def customer_comes(self):
        if self.customer_x != 430:
            self.customer_x += 2
            self.cafe_win.lblCustomer.setGeometry(QtCore.QRect(self.customer_x, 114, 135, 163))
        else:
            self.customer_timer.stop()
            self.get_order()

    def get_order(self):
        r = random.randint(0, len(self.options)-1)
        order = self.options[r]
        self.cafe_win.lblOrder.setText(order)
        self.cafe_win.lblOrder.setHidden(False)
        self.cafe_win.lblThink.setHidden(False)
        if self.waiter_x == 430:
            self.order(order)

    def order(self, what):
        self.order_timer = QTimer()
        if what == "🍔":
            self.order_details['fetch_x'] = 100
            self.order_details['ready_x'] = 146
            self.order_details['pt'] = 2000
            self.order_details['lbl'] = self.cafe_win.lblHambReady
            self.order_details['fee'] = self.hamb_fee

        elif what == "🍟":
            self.order_details['fetch_x'] = 486
            self.order_details['ready_x'] = 532
            self.order_details['pt'] = 3000
            self.order_details['lbl'] = self.cafe_win.lblFriesReady
            self.order_details['fee'] = self.fries_fee

        elif what == "🍕":
            self.order_details['fetch_x'] = 872
            self.order_details['ready_x'] = 918
            self.order_details['pt'] = 10000
            self.order_details['lbl'] = self.cafe_win.lblPizzaReady
            self.order_details['fee'] = self.pizza_fee

        if self.waiter_x != self.order_details['fetch_x'] and self.waiter_y != self.fetch_point_y:
            self.order_timer.timeout.connect(lambda: self.make_order(self.order_details['pt']))
        self.order_timer.start(self.serv_speed)

    def make_order(self, pt):
        if self.waiter_x != self.order_details['fetch_x']:
            if self.waiter_x > self.order_details['fetch_x']:
                self.waiter_x -= 2
            else:
                self.waiter_x += 2
        if self.waiter_y != self.fetch_point_y:
            self.waiter_y += 2
        self.cafe_win.lblWaiter.setGeometry(QtCore.QRect(self.waiter_x, self.waiter_y, 135, 163))

        if self.waiter_x == self.order_details['fetch_x'] and self.waiter_y == self.fetch_point_y:
            self.order_timer.stop()
            self.fetch_timer = QTimer()
            self.fetch_timer.timeout.connect(self.service)
            self.fetch_timer.setSingleShot(True)
            self.fetch_timer.start(pt)

    def service(self):
        self.fetch_timer.stop()
        self.service_timer = QTimer()
        self.order_details["lbl"].setHidden(False)
        self.service_timer.timeout.connect(self.waiter_serves)
        self.service_timer.start(self.serv_speed)

    def waiter_serves(self):
        if self.waiter_x != self.serv_x:
            if self.waiter_x < self.serv_x:
                self.order_details['ready_x'] += 2
                self.waiter_x += 2
            else:
                self.order_details['ready_x'] -= 2
                self.waiter_x -= 2
        if self.waiter_y != self.serv_y:
            self.ready_y -= 2
            self.waiter_y -= 2
        self.cafe_win.lblWaiter.setGeometry(QtCore.QRect(self.waiter_x, self.waiter_y, 135, 163))
        self.order_details['lbl'].setGeometry(QtCore.QRect(self.order_details['ready_x'], self.ready_y, 135, 163))

        if self.waiter_x == self.serv_x and self.waiter_y == self.serv_y:
            self.order_details['lbl'].setHidden(True)
            self.order_details['ready_x'] = 146
            self.ready_y = 760

            self.cash += self.order_details['fee']

            if not self.shoes_bought:
                self.set_color(self.cafe_win.btnBetterShoes, self.shoes_fee)

            self.set_color(self.cafe_win.btnUpgradeHamb, self.hamb_upgrade_fee)
            self.set_color(self.cafe_win.btnOpenFrier, self.open_frier_fee)
            self.set_color(self.cafe_win.btnUpgradeFries, self.fries_upgrade_fee)
            self.set_color(self.cafe_win.btnOpenOven, self.open_oven_fee)
            self.set_color(self.cafe_win.btnUpgradePizza, self.pizza_upgrade_fee)

            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")
            self.service_timer.stop()
            self.cafe_win.lblOrder.setHidden(True)
            self.cafe_win.lblThink.setHidden(True)
            self.done_timer = QTimer()
            self.done_timer.timeout.connect(self.customer_goes)
            self.done_timer.start(4)

    def customer_goes(self):
        if self.customer_x != 1920:
            self.customer_x += 2
            self.cafe_win.lblCustomer.setGeometry(QtCore.QRect(self.customer_x, 114, 135, 163))
        else:
            self.customer_x = -134
            self.done_timer.stop()
            self.new_customer()

    def upgrade_frame(self, what, btn, frm):
        if what == "fries" or what == "pizza":
            if btn.text() == "💢":
                frm[0].setHidden(False)
            else:
                frm[1].setHidden(False)
        else:
            frm.setHidden(False)

    def upgrade(self, fee, upgrade_fee, level, progress, btn, lbl_fee, lbl_level, prg, attribute):
        if self.cash >= upgrade_fee and progress != 100:
            self.cash -= upgrade_fee
            self.set_color(btn, upgrade_fee)
            upgrade_fee *= 2
            fee += fee // 2
            progress += 10
            level += 1
            lbl_fee.setText(f"🪙 £ {fee}")
            btn.setText(f"UPGRADE 🪙 £ {upgrade_fee}")
            if progress == 100:
                lbl_level.setText("Level MAX")
                btn.setText("MAX")
                btn.setStyleSheet("color: rgb(200, 200, 200);")
                btn.setEnabled(False)
            else:
                lbl_level.setText(f"Level {level}")
            prg.setValue(progress)
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")
            setattr(self, f'{attribute}_fee', fee)
            setattr(self, f'{attribute}_upgrade_fee', upgrade_fee)
            setattr(self, f'{attribute}_level', level)
            setattr(self, f'{attribute}_progress', progress)
        else:
            print("You don't have enough money to upgrade this!")

    def set_color(self, btn, upgrade_fee):
        if self.cash >= upgrade_fee and btn.text() != "MAX":
            style = "color: rgb(25, 25, 222);"
        else:
            style = "color: rgb(255, 1, 1);"
        btn.setStyleSheet(style)

    def hide_upgrade(self, frm):
        frm.setHidden(True)

    def open_frier(self):
        if self.cash >= self.open_frier_fee:
            self.cash -= self.open_frier_fee
            self.cafe_win.btnFrier.setText("🫕")
            self.cafe_win.frmOpenFrier.setHidden(True)
            self.cafe_win.lblFriesPic.setHidden(False)
            self.options += "🍟"
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")

    def open_oven(self):
        if self.cash >= self.open_oven_fee:
            self.cash -= self.open_oven_fee
            self.cafe_win.btnOven.setText("🫕")
            self.cafe_win.frmOpenOven.setHidden(True)
            self.cafe_win.lblPizzaPic.setHidden(False)
            self.options += "🍕"
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")

    def shoes(self):
        if self.cash >= self.shoes_fee:
            self.cash -= self.shoes_fee
            self.shoes_bought = True
            self.serv_speed = 5
            self.cafe_win.btnBetterShoes.setEnabled(False)
            self.cafe_win.btnBetterShoes.setStyleSheet("color: rgb(200, 200, 200);")
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")


app = QApplication([])
cafe = Cafe()
cafe.showMaximized()
app.exec_()
