import sys
import subprocess


# PyQt6 yüklü mü kontrol et, değilse otomatik yükle
try:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
        QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea, QHBoxLayout
    )
except ImportError:
    print("PyQt6 kütüphanesi eksik. Otomatik olarak yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
        QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea, QHBoxLayout
    )


# Kağıt türlerine göre kalınlık değerleri (mm/yaprak)
kagit_kalinliklari = {
    "70 gr 1. hamur": 0.7, "80 gr 1. hamur": 0.8, "90 gr 1. hamur": 0.9,
    "110 gr 1. hamur": 1.1, "60 gr Enzo": 0.9, "70 gr Enzo": 1.1,
    "60 gr Ivory": 0.75, "70 gr Ivory": 0.95, "80 gr Ivory": 1.05,
    "80 gr mat kuşe": 0.9, "90 gr mat kuşe": 1.0, "115 gr mat kuşe": 1.2,
    "130 gr mat kuşe": 1.4, "170 gr mat kuşe": 1.8, "200 gr mat kuşe": 2.2,
    "80 gr parlak kuşe": 0.9, "90 gr parlak kuşe": 1.0, "115 gr parlak kuşe": 1.2,
    "130 gr parlak kuşe": 1.4, "170 gr parlak kuşe": 1.8, "200 gr parlak kuşe": 2.2
}


class KitapSirtKalınlıkHesaplayici(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Kitap Sırt Kalınlığı Hesaplayıcı")
        self.setGeometry(200, 200, 600, 600)


        # Başlık etiketi
        self.title_label = QLabel("📖 Kitap Sırt Kalınlığı Hesaplayıcı", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")


        # Sayfa sayısı etiketi ve giriş kutusu
        self.sayfa_label = QLabel("Sayfa Sayısı:", self)
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Örn: 120")


        # Hesapla ve Temizle butonlarını içeren yatay layout
        self.button_hbox = QHBoxLayout()
        
        # Hesapla butonu
        self.button_hesapla = QPushButton("Hesapla", self)
        self.button_hesapla.clicked.connect(self.hesapla)
        self.button_hbox.addWidget(self.button_hesapla)
        
        # Temizle butonu
        self.button_temizle = QPushButton("Temizle", self)
        self.button_temizle.clicked.connect(self.temizle)
        self.button_hbox.addWidget(self.button_temizle)


        # Sonuç tablosu
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Kağıt Türü", "Kalınlık (mm)"])
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 150)


        # ScrollArea ekleyerek tabloyu kaydırılabilir hale getir
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.table)


        # Arayüz Düzeni
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.sayfa_label)
        layout.addWidget(self.entry)
        layout.addLayout(self.button_hbox)
        layout.addWidget(self.scroll_area)


        self.setLayout(layout)


    def veri_dogrula(self, sayfa_sayisi):
        """ Girilen sayfa sayısının geçerli olup olmadığını kontrol eder. """
        if not sayfa_sayisi.isdigit():
            return "Geçersiz giriş! Sayfa sayısı sadece rakam olmalıdır."
        sayfa_sayisi = int(sayfa_sayisi)
        if sayfa_sayisi <= 0:
            return "Sayfa sayısı 0 veya negatif olamaz!"
        return None  # Geçerli giriş


    def hesapla(self):
        """ Sayfa sayısına göre kitap sırt kalınlığını hesaplar ve tabloya ekler """
        sayfa_sayisi = self.entry.text().strip()


        # Veri doğrulama
        hata_mesaji = self.veri_dogrula(sayfa_sayisi)
        if hata_mesaji:
            self.hata_goster(hata_mesaji)
            return


        sayfa_sayisi = int(sayfa_sayisi)
        yaprak_sayisi = sayfa_sayisi / 2  # 2 sayfa = 1 yaprak olarak kabul edilir.


        self.table.setRowCount(len(kagit_kalinliklari))  # Satır sayısını belirle


        for i, (kagit, kalinlik) in enumerate(kagit_kalinliklari.items()):
            sonuc = yaprak_sayisi * kalinlik
            self.table.setItem(i, 0, QTableWidgetItem(kagit))
            self.table.setItem(i, 1, QTableWidgetItem(f"{sonuc:.2f} MM"))


    def temizle(self):
        """ Tabloyu ve giriş kutusunu temizler """
        self.entry.clear()
        self.table.setRowCount(0)


    def hata_goster(self, mesaj):
        """ Kullanıcıya hata mesajını gösterir. """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Hata")
        msg.setText(mesaj)
        msg.exec()


# Uygulamayı başlat
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KitapSirtKalınlıkHesaplayici()
    pencere.show()
    sys.exit(app.exec())
