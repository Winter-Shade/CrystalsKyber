document.getElementById('kyberForm').addEventListener('submit', function(event) {
    const binaryMessage = document.getElementById('binaryMessage').value;
    const binaryRegex = /^[01]+$/; // Regular expression for binary strings

    if (!binaryRegex.test(binaryMessage)) {
        event.preventDefault(); // Stop form submission if invalid
        alert("Please enter a valid binary string (only 0s and 1s).");
    }
});


// script.js
function generateKeys() {
    fetch('/generate_keys', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        // Populate the DOM with keys (A, t, s matrices)
        document.getElementById('A_polynomialDisplay').innerHTML = data.A_html;
        document.getElementById('t_polynomialDisplay').innerHTML = data.t_html;
        document.getElementById('s_polynomialDisplay').innerHTML = data.s_html;

        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    })
    .catch(error => console.error('Error generating keys:', error));

    document.getElementById("matrixSection").style.display = "block";
}

function encryptMessage() {
    const message = document.getElementById('binaryMessage').value;
    fetch('/generate_ciphertext', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ binaryMessage: message }),
    })
    .then(response => response.json())
    .then(data => {
        // Populate the DOM with ciphertext (u and v)
        document.getElementById('u_display').innerHTML = data.u_html;
        document.getElementById('v_display').innerHTML = data.v_html;

        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    })
    .catch(error => console.error('Error encrypting message:', error));

    document.getElementById("matrixSection2").style.display = "block";
}

function decryptMessage(){
    fetch('/decrypt_message', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message_display').innerHTML = data.Message_html;

        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    })
    .catch(error => console.error('Error generating keys:', error));
}

function showPolynomial(matrixName, index, displayId) {
    fetch(`/get_polynomial?matrix=${matrixName}&index=${index}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById(`${matrixName}_polynomialDisplay`).innerHTML = matrixName!='v'?(`Polynomial at ${matrixName}[${index}]: \\(${data.polynomial}\\)`):(`Polynomial ${matrixName}: \\(${data.polynomial}\\)`);
        document.getElementById(`${matrixName}_polynomialDisplay`).style.display = 'block'
        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    })
    .catch(error => console.error('Error fetching polynomial:', error));
}

function openModal() {
    document.getElementById("infoModal").style.display = "block";
    document.body.style.overflow = "hidden"; // Disable scrolling
}

function closeModal() {
    document.getElementById("infoModal").style.display = "none";
    document.body.style.overflow = "auto"; // Enable scrolling
}
function openModal_DES(){
    document.getElementById("infoModal").style.display = "block";
    document.body.style.overflow = "hidden";
}
function openModal_AES(){
    document.getElementById("infoModal").style.display = "block";
    document.body.style.overflow = "hidden";
}