async function startScan() {
    const network = document.getElementById('network').value;
    const ports = document.getElementById('ports').value;
    const resultsDiv = document.getElementById('scan-results');
    
    resultsDiv.innerHTML = "<p>Scanning... Please wait</p>";
    
    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                network: network,
                ports: ports.split(',').map(p => parseInt(p.trim()))
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error("Received non-JSON response");
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayResults(data);
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        console.error('Scan failed:', error);
    }
}