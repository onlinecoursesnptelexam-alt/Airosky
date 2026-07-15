// API Base URL
const API_BASE_URL = 'https://aerosky-institute-vvot.onrender.com';

// Load certificates on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadCertificates();
});

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/certificates/stats`);
        const data = await response.json();
        
        document.getElementById('totalStudents').textContent = data.total_students || 0;
        document.getElementById('totalCertificates').textContent = data.total_certificates || 0;
        document.getElementById('totalPDFs').textContent = data.total_pdfs || 0;
    } catch (error) {
        console.error('Error loading statistics:', error);
        // Set default values if API fails
        document.getElementById('totalStudents').textContent = '0';
        document.getElementById('totalCertificates').textContent = '0';
        document.getElementById('totalPDFs').textContent = '0';
    }
}

// Load all certificates
async function loadCertificates() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/certificates`);
        const certificates = await response.json();
        
        displayCertificates(certificates);
    } catch (error) {
        console.error('Error loading certificates:', error);
        displayCertificates([]);
    }
}

// Display certificates in table
function displayCertificates(certificates) {
    const tableBody = document.getElementById('certificatesTableBody');
    const noCertificates = document.getElementById('noCertificates');
    
    tableBody.innerHTML = '';
    
    if (certificates.length === 0) {
        noCertificates.style.display = 'block';
        return;
    }
    
    noCertificates.style.display = 'none';
    
    certificates.forEach(certificate => {
        const row = document.createElement('tr');
        
        const statusClass = certificate.status === 'Active' ? 'status-active' : 'status-inactive';
        
        row.innerHTML = `
            <td><strong>${certificate.certificate_id}</strong></td>
            <td>${certificate.student_name}</td>
            <td>${certificate.course}</td>
            <td>${formatDate(certificate.issue_date)}</td>
            <td><span class="status-badge ${statusClass}">${certificate.status}</span></td>
            <td>
                <button class="action-btn btn-view" onclick="viewCertificate('${certificate.certificate_id}')">
                    <i class="fa-solid fa-eye"></i> View
                </button>
                <button class="action-btn btn-delete" onclick="deleteCertificate('${certificate.certificate_id}')">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

// Upload certificate form submission
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('certificate_id', document.getElementById('certificateId').value);
    formData.append('student_name', document.getElementById('studentName').value);
    formData.append('father_name', document.getElementById('fatherName').value);
    formData.append('course', document.getElementById('course').value);
    formData.append('duration', document.getElementById('duration').value);
    formData.append('issue_date', document.getElementById('issueDate').value);
    formData.append('certificate_file', document.getElementById('certificateFile').files[0]);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/certificates/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            alert('Certificate uploaded successfully!');
            document.getElementById('uploadForm').reset();
            loadCertificates();
            loadStatistics();
        } else {
            const error = await response.json();
            alert(`Error uploading certificate: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error uploading certificate:', error);
        alert('Error uploading certificate. Please try again.');
    }
});

// View certificate
function viewCertificate(certificateId) {
    // Open verification page with the certificate ID
    window.open(`veryfication/verify.html?certificate_id=${certificateId}`, '_blank');
}

// Delete certificate
async function deleteCertificate(certificateId) {
    if (!confirm(`Are you sure you want to delete certificate ${certificateId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/certificates/${certificateId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Certificate deleted successfully!');
            loadCertificates();
            loadStatistics();
        } else {
            const error = await response.json();
            alert(`Error deleting certificate: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error deleting certificate:', error);
        alert('Error deleting certificate. Please try again.');
    }
}

// Search functionality
document.getElementById('searchBtn').addEventListener('click', searchCertificates);
document.getElementById('searchInput').addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        searchCertificates();
    }
});

async function searchCertificates() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    
    if (!searchTerm) {
        loadCertificates();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/certificates/search?q=${encodeURIComponent(searchTerm)}`);
        const certificates = await response.json();
        
        displayCertificates(certificates);
    } catch (error) {
        console.error('Error searching certificates:', error);
        displayCertificates([]);
    }
}
