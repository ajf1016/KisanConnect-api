function createUser() {
    const name = document.getElementById('userName').value;
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => document.getElementById('response').innerText = `User Created: ${JSON.stringify(data)}`)
    .catch(error => console.error('Error:', error));
}

function createBid() {
    const amount = document.getElementById('bidAmount').value;
    const requestID = document.getElementById('requestID').value;
    const userID = document.getElementById('userID').value;
    fetch('/api/bids', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: parseFloat(amount), request_id: requestID, user_id: userID })
    })
    .then(response => response.json())
    .then(data => document.getElementById('response').innerText = `Bid Created: ${JSON.stringify(data)}`)
    .catch(error => console.error('Error:', error));
}

function createContract() {
    const requestID = document.getElementById('contractRequestID').value;
    const bidID = document.getElementById('contractBidID').value;
    const status = document.getElementById('contractStatus').value;
    fetch('/api/contracts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request_id: requestID, bid_id: bidID, status: status })
    })
    .then(response => response.json())
    .then(data => document.getElementById('response').innerText = `Contract Created: ${JSON.stringify(data)}`)
    .catch(error => console.error('Error:', error));
}
