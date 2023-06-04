// Mendengarkan kejadian saat halaman dimuat
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status === 'complete') {
      // Mengirim pesan ke content script untuk memeriksa teks di halaman
      chrome.tabs.sendMessage(tabId, { message: "checkHatespeech", text: "Contoh teks yang ingin diperiksa" });
    }
  });
  
  // Mendengarkan pesan yang dikirim dari content script
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.message === "hatespeechResult") {
      // Melakukan sesuatu dengan hasil pengecekan hatespeech, misalnya menampilkan notifikasi
      if (request.isHatespeech) {
        chrome.notifications.create({
          type: "basic",
          title: "Hatespeech Detected",
          message: "Teks mengandung hatespeech: " + request.censoredText,
          iconUrl: "icon.png"
        });
      }
    }
  });
  