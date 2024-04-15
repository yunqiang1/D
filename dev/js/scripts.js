let audioContext = null;

function createAudioVisualizer(audioSrc, canvas) {
    // Create an audio element
    const audioElement = new Audio(audioSrc);

    // Create a NEW audio context and analyser for each audio element
    const localAudioContext = new AudioContext();
    const analyser = localAudioContext.createAnalyser();
    const source = localAudioContext.createMediaElementSource(audioElement);

    // Connect source to analyser and audio context destination
    source.connect(analyser);
    analyser.connect(localAudioContext.destination);

    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
        requestAnimationFrame(draw);

        analyser.getByteFrequencyData(dataArray);

        const canvasContext = canvas.getContext('2d');
        const WIDTH = canvas.width;
        const HEIGHT = canvas.height;

        canvasContext.fillStyle = 'rgb(0, 0, 0)';
        canvasContext.fillRect(0, 0, WIDTH, HEIGHT);

        const barWidth = (WIDTH / bufferLength) * 2.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            barHeight = dataArray[i];

            canvasContext.fillStyle = 'rgb(' + (barHeight + 100) + ',50,50)';
            canvasContext.fillRect(x, HEIGHT - barHeight / 2, barWidth, barHeight / 2);

            x += barWidth + 1;
        }
    }

    draw();

    return { audioElement, audioContext: localAudioContext };    // Return both the audio element and its associated audio context
}



window.onload = function () {
    fetch('../php/api.php')
        .then(response => response.json())
        .then(data => {
            const tableElement = document.getElementById('recordings-list');
            data.forEach(recording => {
                const row = tableElement.insertRow();
            
                // Audio visualizer column
                const audioVisualizerCell = row.insertCell(0);
                const canvas = document.createElement('canvas');
                canvas.width = 200;  // 设置为200像素宽
                canvas.height = 150;  // 设置为150像素高
                canvas.className = 'audio-visualizer';
                audioVisualizerCell.appendChild(canvas);
            
                const { audioElement, audioContext: currentAudioContext } = createAudioVisualizer(recording.file_path, canvas);
            




                // Play/Pause button column
                const playPauseCell = row.insertCell(1);
                const playImg = document.createElement('img');
                playImg.src = "../data/logo/260.png";
                playImg.className = 'play-icon';
                const pauseImg = document.createElement('img');
                pauseImg.src = "../data/logo/1.png";
                pauseImg.className = 'pause-icon';
                pauseImg.style.display = "none";  // Initially hidden
                playPauseCell.className = 'centered-content no-border';



                playImg.onclick = function() {
                    // Here, try to resume the AudioContext if it's in suspended state
                    if (currentAudioContext && currentAudioContext.state === "suspended") {
                        currentAudioContext.resume().then(() => {
                            console.log('AudioContext resumed successfully.');
                        });
                    }
                
                    audioElement.play();  // 播放音频
                    playImg.style.display = "none";
                    pauseImg.style.display = "block";
                };
                

                pauseImg.onclick = function () {
                    audioElement.pause();  // 暂停音频
                    playImg.style.display = "block";
                    pauseImg.style.display = "none";
                };

                playPauseCell.appendChild(playImg);
                playPauseCell.appendChild(pauseImg);

                // Recording timestamp column
                const timestampCell = row.insertCell(2);
                timestampCell.textContent = recording.timestamp;

                // Audio duration column
                const durationCell = row.insertCell(3);
                durationCell.textContent = recording.duration;

                // Notes column
                const notesCell = row.insertCell(4);
                notesCell.textContent = recording.notes || "-";

                // Transcribed text column
                const transcribedTextCell = row.insertCell(5);
                transcribedTextCell.textContent = recording.transcribed_text || "-";

                // Transcription time column
                const transcriptionTimeCell = row.insertCell(6);
                transcriptionTimeCell.textContent = recording.transcription_time || "-";

                // Action buttons column
                const actionsCell = row.insertCell(7);
                actionsCell.textContent = "Action Buttons";  // 这里可以添加实际的操作按钮
            });
        })
        .catch(error => {
            console.error('Error fetching recordings:', error);
        });
};
