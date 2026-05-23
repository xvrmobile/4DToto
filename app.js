const video = document.getElementById('webcam');
const snapBtn = document.getElementById('snap-btn');
const saveBtn = document.getElementById('save-btn');
const resultPanel = document.getElementById('result-panel');
const outputText = document.getElementById('output-text');

// 1. Activate Smartphone Back Camera View Stream
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(stream => { video.srcObject = stream; })
    .catch(err => { alert("Camera access blocked or unavailable: " + err); });

// 2. Capture Photo Frame and process Text
snapBtn.addEventListener('click', async () => {
    snapBtn.innerText = "⚡ Scanning Ticket Layout...";
    snapBtn.disabled = true;

    // Create a hidden canvas memory buffer to lock the image frame
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Process using Tesseract.js directly on phone client memory
    try {
        const result = await Tesseract.recognize(canvas, 'eng');
        outputText.value = result.data.text;
        resultPanel.style.display = 'block';
    } catch (error) {
        alert("OCR Scan Interrupted: " + error);
    } finally {
        snapBtn.innerText = "📷 Snap & Scan Ticket";
        snapBtn.disabled = false;
    }
});

// 3. Save to local browser cache (Privacy Safe, 100% Free)
saveBtn.addEventListener('click', () => {
    const rawLines = outputText.value;
    
    // Quick regex formula to identify strings of 4 consecutive numbers (4D numbers)
    const numbersFound = rawLines.match(/\b\d{4}\b/g) || [];
    
    if(numbersFound.length === 0) {
        alert("No valid 4D patterns recognized. Please manually type them in the box first.");
        return;
    }

    let savedBets = JSON.parse(localStorage.getItem('my_tracked_bets')) || [];
    savedBets.push({
        numbers: numbersFound,
        date_scanned: new Date().toLocaleDateString()
    });

    localStorage.setItem('my_tracked_bets', JSON.stringify(savedBets));
    alert(`Successfully registered ${numbersFound.length} numbers onto your device storage!`);
});
