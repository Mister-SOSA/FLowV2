document.addEventListener('DOMContentLoaded', function () {
    const modifiedAtSpans = document.querySelectorAll('.modified_at');

    modifiedAtSpans.forEach(span => {
        const epoch = parseInt(span.textContent);
        if (!isNaN(epoch)) {
            const now = Math.floor(Date.now() / 1000);
            const secondsAgo = now - epoch;

            let timeAgo;
            if (secondsAgo < 60) {
                timeAgo = 'just now';
            } else if (secondsAgo < 3600) {
                const minutes = Math.floor(secondsAgo / 60);
                timeAgo = `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
            } else if (secondsAgo < 86400) {
                const hours = Math.floor(secondsAgo / 3600);
                timeAgo = `${hours} hour${hours !== 1 ? 's' : ''} ago`;
            } else if (secondsAgo < 604800) {
                const days = Math.floor(secondsAgo / 86400);
                timeAgo = `${days} day${days !== 1 ? 's' : ''} ago`;
            } else if (secondsAgo < 2629746) {
                const weeks = Math.floor(secondsAgo / 604800);
                timeAgo = `${weeks} week${weeks !== 1 ? 's' : ''} ago`;
            } else if (secondsAgo < 31556952) {
                const months = Math.floor(secondsAgo / 2629746);
                timeAgo = `${months} month${months !== 1 ? 's' : ''} ago`;
            } else {
                const years = Math.floor(secondsAgo / 31556952);
                timeAgo = `${years} year${years !== 1 ? 's' : ''} ago`;
            }

            span.textContent = timeAgo;
        } else {
            console.error('Invalid epoch time:', span.textContent);
        }
    });
});
