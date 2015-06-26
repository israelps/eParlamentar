/**
 * Created by Israel P. Siqueira on 25/06/2015.
 */
var randomScalingFactor = function () {
    return Math.round(Math.random() * 100)
};
var data = {
    labels: ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", "Julho"],
    datasets: [

        {
            fillColor: "rgba(255,0,0,0.5)",
            strokeColor: "rgba(255,0,0,0.8)",
            highlightFill: "rgba(255,0,0,0.75)",
            highlightStroke: "rgba(255,0,0,1)",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
}
window.onload = function () {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myBar = new Chart(ctx).Line(data, {
        responsive: true,
        belzierCurve: false
    });
}
