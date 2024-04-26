
document.addEventListener('DOMContentLoaded', function () {
    const sampleLabels = document.querySelectorAll('.channel.sample');
    let currentAudio = null;
    let currentLabel = null;

    sampleLabels.forEach(label => {
        label.addEventListener('click', () => handleSampleClick(label));
    });

    function handleSampleClick(label) {
        resetCurrentAudio(label);
        togglePlay(label);
    }

    function resetCurrentAudio(label) {
        // Remove the playing class and stop audio if a different label is clicked
        if (currentLabel && currentLabel !== label) {
            currentLabel.classList.remove('sample-playing');
            currentAudio.pause();
            currentAudio.currentTime = 0;
        }
    }

    function togglePlay(label) {
        if (label.audio) {
            // Toggle play/pause for the current label
            if (label.audio.paused) {
                playAudio(label.audio, label);
            } else {
                pauseAudio(label.audio, label);
            }
        } else {
            // Fetch and play new audio if none was attached to this label
            fetchAndPlayAudio(label);
        }
    }

    function playAudio(audio, label) {
        audio.play();
        currentAudio = audio;
        currentLabel = label;
        label.classList.add('sample-playing');
    }

    function pauseAudio(audio, label) {
        audio.pause();
        audio.currentTime = 0;
        label.classList.remove('sample-playing');
        currentAudio = null;
        currentLabel = null;
    }

    function fetchAndPlayAudio(label) {
        const samplePath = label.getAttribute('data-sample-path');
        fetch('/fetch-sample', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sample_path: samplePath })
        })
            .then(response => response.blob())
            .then(blob => createAudioFromBlob(blob, label))
            .catch(error => console.error('Error fetching sample:', error));
    }

    function createAudioFromBlob(blob, label) {
        const audio = new Audio(URL.createObjectURL(blob));
        label.audio = audio;
        audio.play();
        audio.onended = () => endAudio(label);
        playAudio(audio, label);
    }

    function endAudio(label) {
        label.classList.remove('sample-playing');
        currentLabel = null;
    }
});
