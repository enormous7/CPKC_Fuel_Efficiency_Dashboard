document.addEventListener('DOMContentLoaded', function() {
    // Render Monthly Fuel Consumption Chart
    const ctx = document.getElementById('monthlyFuelChart').getContext('2d');

    // monthlyAvgFuelData is passed from Flask in index.html
    const labels = monthlyAvgFuelData.map(d => d.Month);
    const data = monthlyAvgFuelData.map(d => d.Fuel_Consumed_liters);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Fuel Consumed (Liters)',
                data: data,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                pointBackgroundColor: '#007bff',
                pointBorderColor: '#fff',
                pointHoverRadius: 6,
                pointHoverBorderColor: '#007bff',
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Historical Fuel Consumption'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' L';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Fuel Consumed (Liters)'
                    },
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return value.toLocaleString() + ' L';
                        }
                    }
                }
            }
        }
    });
});

async function predictFuel() {
    const distance = document.getElementById('distance').value;
    const speed = document.getElementById('speed').value;
    const weight = document.getElementById('weight').value;
    const weather = document.getElementById('weather').value;

    if (!distance || !speed || !weight || !weather) {
        alert('Please fill in all prediction parameters.');
        return;
    }

    try {
        const response = await fetch('/predict_fuel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                distance_km: parseFloat(distance),
                avg_speed_kmh: parseFloat(speed),
                train_weight_tons: parseFloat(weight),
                weather_condition: parseInt(weather)
            })
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('predictedFuelVal').textContent = parseFloat(result.predicted_fuel).toLocaleString() + ' L';
            document.getElementById('optimizedFuelVal').textContent = parseFloat(result.optimized_fuel).toLocaleString() + ' L';
            document.getElementById('potentialSavingsVal').textContent = parseFloat(result.potential_savings).toLocaleString() + ' L';

            const recommendationList = document.getElementById('recommendationList');
            recommendationList.innerHTML = '';
            result.recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recommendationList.appendChild(li);
            });
        } else {
            alert('Error predicting fuel: ' + result.error);
            console.error('Prediction error:', result.error);
        }
    } catch (error) {
        alert('Could not connect to the prediction service. Please ensure the Flask app is running.');
        console.error('Fetch error:', error);
    }
}