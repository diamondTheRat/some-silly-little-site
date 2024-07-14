const CPU = document.getElementById("cpu");
const RAM = document.getElementById("used-ram");
const FRAM = document.getElementById("free-ram");

fetch("/status")
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
.then(data => {
    const usedRam = Math.round(data["RAM"] * 100);
    const freeRam = Math.round(data["FRAM"] * 100);
    const cpu = Math.round(data["CPU"] * 100);
    
    CPU.innerText = `cpu ${cpu}%`;
    RAM.innerText = `used ram ${usedRam}%`;
    FRAM.innerText = `free ram ${freeRam}%`;
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
});

var ws = new WebSocket("/livestatus");
ws.onmessage = function(event) {
    var metrics = JSON.parse(event.data);
    const usedRam = Math.round(metrics["RAM"] * 100);
    const freeRam = Math.round(metrics["FRAM"] * 100);
    const cpu = Math.round(metrics["CPU"] * 100);

    CPU.innerText = `cpu ${cpu}%`;
    RAM.innerText = `used ram ${usedRam}%`;
    FRAM.innerText = `free ram ${freeRam}%`;
};

ws.onopen = function(event) {
    setInterval(() => {
        ws.send("");
    }, 1000);
}
