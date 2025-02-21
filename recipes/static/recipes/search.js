function toggleChart() {
    const chartContainer = document.getElementById('chart-container');
    const chartColumn = document.getElementById('chart-column');
    const toggleButton = document.getElementById('toggle-chart');

    if (chartContainer.style.display === 'none' || chartContainer.style.display === '') {
        chartContainer.style.display = 'block';
        chartColumn.style.display = 'flex';
        toggleButton.textContent = 'Hide Chart';
    } else {
        chartContainer.style.display = 'none';
        chartColumn.style.display = 'none'; 
        toggleButton.textContent = 'Show Chart';
    }
}