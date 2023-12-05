(function () {
    const timeElement = document.getElementsByClassName("time")[0];

    function loadTimeRemote() {
        fetch('/json', {method: 'get'})
            .then(resp => {
                if (!resp.ok) {
                    throw new Error(resp.statusText);
                }
                return resp.json();
            })
            .then(data => {
                const date = new Date(parseInt(data.time) * 1000);
                timeElement.innerHTML = date.toLocaleString();
            })
            .catch(err => {
                alert(err.message);
            });
    }

    loadTimeRemote();
    setInterval(() => loadTimeRemote(), 1000);
})();