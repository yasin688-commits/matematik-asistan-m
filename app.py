// 1. EKRAN AÇILDIĞINDA YAPILACAKLAR
When Screen1.Initialize:
   set AdMob_Banner.LoadAd to "True"
   set Label_Title.Text to "4. Sınıf Testleri"

// 2. MENÜ BUTONLARI (9 Adet Kart İçin Tek Mantık)
When Card_Testler.Click: open_screen("Testler_Sayfasi")
When Card_Video.Click:  open_screen("Video_Sayfasi")
When Card_Oyun.Click:   open_screen("Oyun_Sayfasi")
When Card_Konu.Click:   open_screen("Konu_Anlatimi_Sayfasi")
When Card_Favori.Click: open_screen("Favoriler_Sayfasi")
When Card_İstatistik.Click: open_screen("Istatistik_Sayfasi")

// 3. HESABIMI SİL (Diyalog Penceresi)
When Card_HesapSil.Click:
   call Notifier1.ShowChooseDialog(
      message = "Hesabınızı silmek istediğinize emin misiniz?",
      title = "UYARI",
      button1Text = "Evet, Sil",
      button2Text = "İptal",
      cancelable = False
   )

When Notifier1.AfterChoosing(choice):
   if choice == "Evet, Sil":
      call Firebase_DB.DeleteUser(UserID)
      show_message("Hesabınız silindi.")

// 4. REKLAMLARI KALDIR BUTONU
When Button_ReklamKaldir.Click:
   call InAppBilling.LaunchPurchaseFlow(productID = "reklam_kaldir_premium")
