from flask import Flask, render_template

app = Flask(__name__)

# Table data
data = [
    {
        "Algorithm": "NTRU",
        "Type": "Asymmetric (Public-Key)",
        "Key Size": "1-2 KB (Public/Private)",
        "Ciphertext Size": "~1 KB",
        "Performance": "Moderate (All operations)",
        "Security Basis": "Lattice-based (Quantum-Secure)",
        "Quantum Resistance": "Yes",
        "Ciphertext Expansion": "High",
        "Bulk Data Suitability": "No (Inefficient)",
        "Typical Use Case": "Key exchange, Signatures",
    },
    {
        "Algorithm": "Kyber",
        "Type": "Asymmetric (Public-Key)",
        "Key Size": "1-2 KB (Public/Private)",
        "Ciphertext Size": "~800 B",
        "Performance": "Fast (All operations)",
        "Security Basis": "Lattice-based (Quantum-Secure)",
        "Quantum Resistance": "Yes",
        "Ciphertext Expansion": "Moderate",
        "Bulk Data Suitability": "No (Inefficient)",
        "Typical Use Case": "Key exchange, Encryption",
    },
    {
        "Algorithm": "AES",
        "Type": "Symmetric (Shared-Key)",
        "Key Size": "128, 192, or 256 bits",
        "Ciphertext Size": "Same as plaintext",
        "Performance": "Extremely fast",
        "Security Basis": "Substitution-permutation",
        "Quantum Resistance": "No",
        "Ciphertext Expansion": "None",
        "Bulk Data Suitability": "Yes",
        "Typical Use Case": "Encrypting large data",
    },
    {
        "Algorithm": "DES",
        "Type": "Symmetric (Shared-Key)",
        "Key Size": "56 bits (Effective Key Size)",
        "Ciphertext Size": "Same as plaintext",
        "Performance": "Fast (But outdated)",
        "Security Basis": "Substitution-permutation",
        "Quantum Resistance": "No",
        "Ciphertext Expansion": "None",
        "Bulk Data Suitability": "No (Weak and Outdated)",
        "Typical Use Case": "Deprecated",
    },
]

@app.route("/")
def index():
    return render_template("table.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
