const websocket = new WebSocket('ws://192.168.0.105:8000/ws/dashboard/')

websocket.onopen = function (e) {
    websocket.send(JSON.stringify({
        'message': 'welcome',
    }))
}

websocket.onmessage = function (e) {
    console.log(e.data)
}

const fetchDashboardData = async () => {
    const response = await fetch('http://192.168.0.105:8000/dashboardData')
    const data = await response.json()
    return data
}


async function draw() {
    const data = await fetchDashboardData()
    const {x, y} = data
    new Chart("myChart", {
        type: "line",
        data: {
            labels: x,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "rgb(255,0,0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: y
            }]
        },
        options: {
            legend: {display: false},
            scales: {
                yAxes: [{ticks: {min: 60, max: 150}}],
            }
        }
    });
}

draw()