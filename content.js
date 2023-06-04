chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.message === "checkHatespeech") {
      var textNodes = document.evaluate("//text()", document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
      for (var i = 0; i < textNodes.snapshotLength; i++) {
        var node = textNodes.snapshotItem(i);
        var content = node.textContent;
        // Kirim permintaan ke API Django untuk memeriksa kata-kata hatespeech
        fetch('http://localhost:8000/api/check_hatespeech/', {
          method: 'POST',
          body: JSON.stringify({ text: content }),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Original Content:", content);
          if (data.is_hatespeech) {
            // Sensor kata-kata hatespeech dengan menggantikan dengan tanda bintang
            var censoredContent = content.replace(/(\b\S+hatespeech\S+\b)/gi, '***');
            node.textContent = censoredContent;
          }
        });
      }
    }
  });
  
  chrome.runtime.sendMessage({ message: "censor_hatespeech" });
  