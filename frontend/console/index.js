const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;
const mainUrl = `${protocol}//${hostname}${port ? `:${port}` : ''}`;
const consoleUrl = `${mainUrl}/console`;
const consoleOutputUrl = `${consoleUrl}/output`;
const consoleInputUrl = `${consoleUrl}/run`;

const consoleContainer = document.getElementById("console-container");

const currentDirectory = document.getElementById("cwd");
const input = document.getElementById("console-input");

const ERROR = 0;
const OK = 1;
const USER = 2;

var current_path = "";
var previous_commands = [""];
var command_index = 1;

function updateInput(command) {
    input.value = command;
}

function updateOutput() {
    fetch(consoleOutputUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        consoleContainer.innerHTML = '';
        var lines = data["output"];
        var cwd = data["cwd"];
        currentDirectory.innerText = cwd + " > ";
        var commands = [];
        for(let i = 0; i < lines.length; i++) {
            const line = lines[i];

            if(line[0] === OK || line[0] === ERROR) {
                var span = document.createElement('span');
                span.innerText = line[1];
                span.className = line[0] == OK ? "text-ok" : "text-error";
                consoleContainer.appendChild(span);
            } else if(line[0] === USER) {
                var path = document.createElement('span');
                path.innerText = line[1] + " > ";
                path.className = "text-path";
                consoleContainer.appendChild(path);
                    
                var cmd = document.createElement('span');
                cmd.innerText = line[2];
                cmd.className = "text-ok";
                path.appendChild(cmd);
                commands.push(line[2]);
            }
        }
        previous_commands = commands;
        command_index = commands.length;
        document.documentElement.scrollTop = document.documentElement.scrollHeight;
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}
updateOutput();


function enteredCommand(e, element){
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code === 13) { //Enter keycode
        fetch(consoleInputUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({command: element.value})
        });
        element.value = "";
        updateOutput();
    }
    command_index = previous_commands.length;
}

document.addEventListener("keydown", function(event) {
    if (event.key === "ArrowUp") {
        command_index--;
        if (command_index >= 0) {
            updateInput(previous_commands[command_index]);
        }
    } else if (event.key === "ArrowDown") {
        command_index++;
        if (command_index < previous_commands.length) {
            updateInput(previous_commands[command_index]);
        }
    }
});