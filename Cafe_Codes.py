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

        self.cash = 0
        self.options = "🍔"

        self.serv_speed = 10
        self.shoes_fee = 400

        self.serv_x = 430
        self.serv_y = 330

        self.waiter_x = 430
        self.waiter_y = 330
        self.customer_x = -134

        self.order_details = dict()

        self.fetch_point_y = 744

        self.ready_y = 760

        self.hamburger_fee = 3
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

        self.cafe_win.btnToaster.clicked.connect(lambda: self.upgrade_frame("hamburger", self.cafe_win.frmUpgradeHamburgers))
        self.cafe_win.btnUpgradeHamb.clicked.connect(self.upgrade_hamburgers)
        self.cafe_win.btnCloseHamb.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmUpgradeHamburgers))

        self.cafe_win.btnFrier.clicked.connect(lambda: self.upgrade_frame("fries", [self.cafe_win.frmOpenFrier, self.cafe_win.frmUpgradeFries]))
        self.cafe_win.btnUpgradeFries.clicked.connect(self.upgrade_fries)
        self.cafe_win.btnCloseFries.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmUpgradeFries))
        self.cafe_win.btnOpenFrier.clicked.connect(self.open_frier)
        self.cafe_win.btnCloseFrier.clicked.connect(lambda: self.hide_upgrade(self.cafe_win.frmOpenFrier))

        self.cafe_win.btnOven.clicked.connect(lambda: self.upgrade_frame("pizza", [self.cafe_win.frmOpenOven, self.cafe_win.frmUpgradePizza]))
        self.cafe_win.btnUpgradePizza.clicked.connect(self.upgrade_pizza)
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
            self.order_details['fee'] = self.hamburger_fee

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

            if self.cash >= self.shoes_fee:
                self.cafe_win.btnBetterShoes.setStyleSheet("color: rgb(25, 25, 222);")
            else:
                self.cafe_win.btnBetterShoes.setStyleSheet("color: rgb(255, 1, 1);")

            if self.cash >= self.hamb_upgrade_fee and self.cafe_win.btnUpgradeHamb.text() != "MAX":
                self.cafe_win.btnUpgradeHamb.setStyleSheet("color: rgb(25, 25, 222);")
            if self.cash >= self.open_frier_fee:
                self.cafe_win.btnOpenFrier.setStyleSheet("color: rgb(25, 25, 222);")
            if self.cash >= self.fries_upgrade_fee and self.cafe_win.btnUpgradeFries.text() != "MAX":
                self.cafe_win.btnUpgradeFries.setStyleSheet("color: rgb(25, 25, 222);")
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

    def upgrade_frame(self, what, frm):
        if what == "fries" or what == "pizza":
            if self.cafe_win.btnFrier.text() == "💢":
                frm[0].setHidden(False)
            else:
                frm[1].setHidden(False)
        else:
            frm.setHidden(False)

    def upgrade_hamburgers(self):
        if self.cash >= self.hamb_upgrade_fee and self.hamb_progress != 100:
            self.cash -= self.hamb_upgrade_fee
            if self.cash <= self.hamb_upgrade_fee and self.cafe_win.btnUpgradeHamb.text() != "MAX":
                self.cafe_win.btnUpgradeHamb.setStyleSheet("color: rgb(255, 1, 1);")
            self.hamb_upgrade_fee *= 2
            self.hamburger_fee += self.hamburger_fee // 2
            self.hamb_progress += 10
            self.hamb_level += 1
            self.cafe_win.lblHambFee.setText(f"🪙 £ {self.hamburger_fee}")
            self.cafe_win.btnUpgradeHamb.setText(f"UPGRADE 🪙 £ {self.hamb_upgrade_fee}")
            if self.hamb_progress == 100:
                self.cafe_win.lblHambLevel.setText("Level MAX")
                self.cafe_win.btnUpgradeHamb.setText("MAX")
                self.cafe_win.btnUpgradeHamb.setStyleSheet("color: rgb(200, 200, 200);")
                self.cafe_win.btnUpgradeHamb.setEnabled(False)
            else:
                self.cafe_win.lblHambLevel.setText(f"Level {self.hamb_level}")
            self.cafe_win.prgHambLevel.setValue(self.hamb_progress)
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")
        else:
            print("You don't have enough money to upgrade this!")

    def upgrade_fries(self):
        if self.cash >= self.fries_upgrade_fee and self.fries_progress != 100:
            self.cash -= self.fries_upgrade_fee
            if self.cash <= self.fries_upgrade_fee and self.cafe_win.btnUpgradeFries.text() != "MAX":
                self.cafe_win.btnUpgradeFries.setStyleSheet("color: rgb(255, 1, 1);")
            self.fries_upgrade_fee *= 2
            self.fries_fee += self.fries_fee // 2
            self.fries_progress += 10
            self.fries_level += 1
            self.cafe_win.lblFriesFee.setText(f"🪙 £ {self.fries_fee}")
            self.cafe_win.btnUpgradeFries.setText(f"UPGRADE 🪙 £ {self.fries_upgrade_fee}")
            if self.fries_progress == 100:
                self.cafe_win.lblFriesLevel.setText("Level MAX")
                self.cafe_win.btnUpgradeHamb.setText("MAX")
                self.cafe_win.btnUpgradeFries.setStyleSheet("color: rgb(200, 200, 200);")
                self.cafe_win.btnUpgradeFries.setEnabled(False)
            else:
                self.cafe_win.lblFriesLevel.setText(f"Level {self.fries_level}")
            self.cafe_win.prgFriesLevel.setValue(self.fries_progress)
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")
        else:
            print("You don't have enough money to upgrade this!")

    def upgrade_pizza(self):
        if self.cash >= self.pizza_upgrade_fee and self.pizza_progress != 100:
            self.cash -= self.pizza_upgrade_fee
            if self.cash <= self.pizza_upgrade_fee and self.cafe_win.btnUpgradePizza.text() != "MAX":
                self.cafe_win.btnUpgradePizza.setStyleSheet("color: rgb(255, 1, 1);")
            self.pizza_upgrade_fee *= 2
            self.pizza_fee += self.pizza_fee // 2
            self.pizza_progress += 10
            self.pizza_level += 1
            self.cafe_win.lblPizzaFee.setText(f"🪙 £ {self.pizza_fee}")
            self.cafe_win.btnUpgradePizza.setText(f"UPGRADE 🪙 £ {self.pizza_upgrade_fee}")
            if self.pizza_progress == 100:
                self.cafe_win.lblPizzaLevel.setText("Level MAX")
                self.cafe_win.btnUpgradeHamb.setText("MAX")
                self.cafe_win.btnUpgradePizza.setStyleSheet("color: rgb(200, 200, 200);")
                self.cafe_win.btnUpgradePizza.setEnabled(False)
            else:
                self.cafe_win.lblPizzaLevel.setText(f"Level {self.pizza_level}")
            self.cafe_win.prgPizzaLevel.setValue(self.pizza_progress)
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")
        else:
            print("You don't have enough money to upgrade this!")

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
            self.serv_speed = 5
            self.cafe_win.btnBetterShoes.setEnabled(False)
            self.cafe_win.btnBetterShoes.setStyleSheet("color: rgb(200, 200, 200);")
            self.cafe_win.lblMoney.setText(f"🪙 £ {self.cash}")


app = QApplication([])
cafe = Cafe()
cafe.showMaximized()
app.exec_()
