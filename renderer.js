// This file is required by the index.html file.
const { dialog } = require('electron').remote;
const chart = require('chart.js');
const pyshell = require('python-shell');
const fs = require('fs')

let directedDmaPlotAreaEL = document.getElementById('plot-area');
let directedDmaPlaceholderEl = document.getElementById('plot-placeholder');
// let saveRecordBtnEl = document.getElementById('saveProcessedRecord');
let openedRecordPathEl = document.getElementById('wiiBoardRecordPath');
let savedRecordPathEl = document.getElementById('savedRecordPath');

document.getElementById('openWiiBoardRecord').onclick = () => {
    setElementsInitialState();
    dialog.showOpenDialog({
        title: 'Open Wii Board csv record',
        filters: [
            { name: 'Raw/Processed Wii Board Data', extensions: ['csv', 'json'] },
            { name: 'Raw Wii Board Data', extensions: ['csv'] },
            { name: 'Processed Wii Board Data', extensions: ['json'] }],
        properties: ['openFile']
    }, filePaths => {
        if (filePaths) {
            if (!filePaths) return;

            targetFilePath = filePaths[0];
            processRecordInPython(targetFilePath, plotDirectedDma);

            openedRecordPathEl.textContent = `Opened ${targetFilePath}`;
            openedRecordPathEl.hidden = false;
            directedDmaPlaceholderEl.hidden = false;
        }
    });
};

function setElementsInitialState() {
    openedRecordPathEl.hidden = true;
    savedRecordPathEl.hidden = true;
    directedDmaPlotAreaEL.hidden = true;
    directedDmaPlaceholderEl.hidden = true;
    // saveRecordBtnEl.setAttribute('disabled', true);
}

function processRecordInPython(filePath, successCallback) {
    if (filePath.includes('.json')) {
        fs.readFile(filePath, (err, jsonStr) => {
            if (err) { alert(err); return; }
            let processedData = JSON.parse(jsonStr);
            successCallback(processedData.directedDma.angle, processedData.directedDma.alpha);
            directedDmaPlaceholderEl.hidden = true;
        });
    } else if (filePath.includes('.csv')) {
        pyshell.PythonShell.run(`${__dirname}/python_files/entry.py`, {
            args: [filePath]
        }, (err, output) => {
            directedDmaPlaceholderEl.hidden = true;
            if (err) {
                alert(`${err.exitCode} | ${err.traceback}`);
                return;
            }
            savedFilePath = output[0]
            fs.readFile(savedFilePath, (err, jsonStr) => {
                if (err) alert(err);
                savedRecordPathEl.hidden = false;
                savedRecordPathEl.textContent = `Saved to ${savedFilePath}`;
                let processedData = JSON.parse(jsonStr);
                successCallback(processedData.directedDma.angle, processedData.directedDma.alpha);
            });
        });
    }
}

function plotDirectedDma(angle_vect, alpha_vect) {
    // saveRecordBtnEl.removeAttribute('disabled');
    directedDmaPlotAreaEL.hidden = false;
    new chart.Chart(document.getElementById('directedDmaPlot'), setupChartConfig({
        type: 'line',
        color: '#5b8cac',
        x: alpha_vect,
        y: angle_vect,
        xLabel: 'Angle, degree',
        yLabel: 'Alpha',
        title: 'Directed DMA'
    }));
}

function setupChartConfig(simpleConfig) {
    return {
        type: simpleConfig.type,
        data: {
            labels: simpleConfig.y,
            datasets: [{
                label: simpleConfig.title,
                backgroundColor: simpleConfig.color,
                borderColor: simpleConfig.color,
                data: simpleConfig.x,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.3,
            title: {
                display: false,
                text: ''
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: simpleConfig.xLabel
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: simpleConfig.yLabel
                    }
                }]
            }
        }
    };
}

// let copPlot = new chart.Chart(
//     document.getElementById('statokinesiogram'),
//     setupChartConfig({
//         type: 'line',
//         color: 'red',
//         x: cop.x,
//         y: cop.y,
//         xLabel: 'X, cm',
//         yLabel: 'Y, xm',
//         title: 'CoP'
//     }));

/*
saveRecordBtnEl.onclick = () => {
    let data = localStorage.getItem('lastProcessedRecord');
    let filePath = localStorage.getItem('lastOpenedFilePath');
    let newFilePath = `${filePath.split('.')[0]}.json`;

    fs.writeFile(newFilePath, data, (err) => {
        if (err) alert(err);
        savedRecordPathEl.textContent = `Saved to ${newFilePath}`;
        savedRecordPathEl.hidden = false;
    });

    // dialog.showSaveDialog({
    //     title: 'Save processed Wii Board record',
    //     filters: [{ name: 'csv', extensions: ['csv'] }]
    // }, filePath => {
    //     if (filePath) {
    //     }
    // });
}
*/