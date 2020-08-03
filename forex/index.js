//1. Define chart properties
//2. Create chart with defined properites and bind it to the DOM element
//3. Add the CandleStick Series
//4. Set the data and render

const log = console.log;

const chartProperties ={
    width:1500,
    height:600,
    timeScale:{
        timeVisible:true,
        secondsVisible:false,
    }
}

const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();


fetch('https://api.binance.com//api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000')
    .then(res => res.json())
    .then(data => {
        const cdata = data.map(d => {
            return {time:d[0]/1000,
                open:parseFloat(d[1]),
                high:parseFloat(d[2]),
                low:parseFloat(d[3]),
                close:parseFloat(d[4])}
        });
        candleSeries.setData(cdata);
    })
    .catch(err => log(err))

