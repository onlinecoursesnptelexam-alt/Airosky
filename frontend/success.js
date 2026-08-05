/* ============================================================
   AIROSKY SUCCESS PAGE
   success.js
   Complete Production-Ready Implementation

============================================================ */

/* ============================================================
   CONFIGURATION
============================================================ */

// Use the local backend during development
const API_BASE_URL = "https://aerosky-institute-vvot.onrender.com";

/* ============================================================
   DOM ELEMENTS
============================================================ */

const loaderScreen = document.getElementById("loaderScreen");
const successScreen = document.getElementById("successScreen");
const percentText = document.getElementById("percent");
const loadingTitle = document.getElementById("loadingTitle");
const loadingText = document.getElementById("loadingText");
const registrationNumber = document.getElementById("registrationNumber");
const downloadBtn = document.getElementById("downloadBtn");
const homeBtn = document.getElementById("homeBtn");
const confettiCanvas = document.getElementById("confetti");
const statusMessage = document.getElementById("statusMessage");

/* ============================================================
   SVG CIRCLE
============================================================ */

const progressCircle = document.querySelector(".loader-progress");
const radius = 70;
const circumference = 2 * Math.PI * radius;
progressCircle.style.strokeDasharray = circumference;
progressCircle.style.strokeDashoffset = circumference;

/* ============================================================
   CONFIG
============================================================ */

const CONFIG = {
    duration: 2500,
    messageInterval: 800,
    confettiDuration: 3000
};

/* ============================================================
   LOADING MESSAGES
============================================================ */

const loadingSteps = [
    {
        title: "Preparing your Registration",
        text: "Please wait while we securely process your enrollment."
    },
    {
        title: "Generating Registration PDF",
        text: "Creating your admission document."
    },
    {
        title: "Verifying Student Details",
        text: "Validating submitted information."
    },
    {
        title: "Finalizing Registration",
        text: "Almost done. Preparing your dashboard."
    },
    {
        title: "Welcome to AIROSKY",
        text: "Everything is ready."
    }
];

/* ============================================================
   STATE VARIABLES
============================================================ */

let progress = 0;
let currentMessage = 0;
let progressTimer = null;
let messageTimer = null;
let confettiTimer = null;
let confettiAnimationId = null;

/* ============================================================
   HELPER FUNCTIONS
============================================================ */

function updateProgressCircle(percent) {
    const offset = circumference - (percent / 100) * circumference;
    progressCircle.style.strokeDashoffset = offset;
}

function updatePercent() {
    percentText.textContent = progress + "%";
    updateProgressCircle(progress);
}

function changeLoadingMessage() {
    if (currentMessage < loadingSteps.length) {
        loadingTitle.textContent = loadingSteps[currentMessage].title;
        loadingText.textContent = loadingSteps[currentMessage].text;
        currentMessage++;
    }
}

function clearAllTimers() {
    if (progressTimer) {
        clearInterval(progressTimer);
        progressTimer = null;
    }
    if (messageTimer) {
        clearInterval(messageTimer);
        messageTimer = null;
    }
    if (confettiTimer) {
        clearTimeout(confettiTimer);
        confettiTimer = null;
    }
    if (confettiAnimationId) {
        cancelAnimationFrame(confettiAnimationId);
        confettiAnimationId = null;
    }
}

/* ============================================================
   LOADER FUNCTIONS
============================================================ */

function startProgress() {
    progress = 0;
    updatePercent();
    
    const intervalTime = CONFIG.duration / 100;
    
    progressTimer = setInterval(() => {
        progress++;
        
        if (progress > 100) {
            progress = 100;
        }
        
        updatePercent();
        
        if (progress >= 100) {
            clearInterval(progressTimer);
            progressTimer = null;
            onLoadingComplete();
        }
    }, intervalTime);
}

function startMessageAnimation() {
    changeLoadingMessage();
    
    messageTimer = setInterval(() => {
        changeLoadingMessage();
    }, CONFIG.messageInterval);
}

function onLoadingComplete() {
    // Don't transition immediately - wait for backend response
    // The transition will be triggered by submitFormInBackground when it completes
    clearAllTimers();
}

/* ============================================================
   TRANSITION FUNCTIONS
============================================================ */

function transitionToSuccess() {
    try {
        loaderScreen.style.opacity = "0";
        loaderScreen.style.transition = "opacity 0.5s ease";

        setTimeout(() => {
            loaderScreen.style.display = "none";
            successScreen.style.display = "flex";
            successScreen.style.opacity = "0";

            setTimeout(() => {
                successScreen.style.opacity = "1";
                successScreen.style.transition = "opacity 0.5s ease";
                startConfetti();
            }, 50);
        }, 500);
    } catch (error) {
        console.error("Transition error:", error);
    }
}

/* ============================================================
   STUDENT DATA
============================================================ */

function getStudentData() {
    return {
        registration: localStorage.getItem("registrationNumber") || "AIR-000000-00000",
        pdf: localStorage.getItem("pdfUrl") || "",
        student: localStorage.getItem("studentName") || "Student",
        email: localStorage.getItem("studentEmail") || "",
        status: localStorage.getItem("registrationStatus") || "processing"
    };
}

function updateRegistrationNumber() {
    try {
        const data = getStudentData();
        registrationNumber.textContent = data.registration;
    } catch (error) {
        console.error("Error updating registration number:", error);
        registrationNumber.textContent = "AIR-000000-00000";
    }
}

function setProcessingState(message) {
    if (statusMessage) {
        statusMessage.textContent = message;
    }

    if (downloadBtn) {
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Preparing PDF...';
    }
}

function setDownloadReady() {
    if (downloadBtn) {
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Registration PDF';
    }
}

async function pollEnrollmentStatus() {
    try {
        const registrationNumberValue = localStorage.getItem("registrationNumber");
        if (!registrationNumberValue) {
            return;
        }

        const response = await fetch(`${API_BASE_URL}/enrollment-status/${encodeURIComponent(registrationNumberValue)}`);
        const result = await response.json();

        if (result.status === "completed") {
            localStorage.setItem("registrationStatus", "success");
            localStorage.setItem("pdfUrl", result.pdf_url || "");
            if (result.pdf_filename) {
                localStorage.setItem("pdfFilename", result.pdf_filename);
            }
            updateRegistrationNumber();
            if (statusMessage) {
                statusMessage.textContent = "Your PDF is ready. You can download it now.";
            }
            setDownloadReady();
            transitionToSuccess();
            return;
        }

        if (result.status === "failed") {
            localStorage.setItem("registrationStatus", "error");
            if (statusMessage) {
                statusMessage.textContent = "We could not complete your enrollment. Please contact support.";
            }
            setDownloadReady();
            transitionToSuccess();
            return;
        }

        if (statusMessage) {
            statusMessage.textContent = "Your registration is being processed. Your PDF and confirmation email will be ready shortly.";
        }
        setProcessingState("Your registration is being processed. Your PDF and confirmation email will be ready shortly.");
        setTimeout(pollEnrollmentStatus, 1500);
    } catch (error) {
        console.error("Status poll error:", error);
        setTimeout(pollEnrollmentStatus, 1500);
    }
}

/* ============================================================
   BACKGROUND FORM SUBMISSION
============================================================ */

async function submitFormInBackground() {
    try {
        const registrationStatus = localStorage.getItem("registrationStatus");
        if (registrationStatus === "success") {
            console.log("Enrollment already completed");
            return;
        }

        const registrationNumberFromStorage = localStorage.getItem("registrationNumber");
        if (registrationNumberFromStorage) {
            registrationNumber.textContent = registrationNumberFromStorage;
        }

        transitionToSuccess();
    } catch (error) {
        console.error("Success page initialization error:", error);
        transitionToSuccess();
    }
}

/* ============================================================
   BUTTON FUNCTIONS
============================================================ */

function downloadPDF() {
    try {
        const data = getStudentData();
        const filename = localStorage.getItem("pdfFilename") || data.pdf.split('/').pop();
        
        if (filename) {
            downloadBtn.disabled = true;
            downloadBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Downloading...';
            
            fetch(`${API_BASE_URL}/download-pdf/${encodeURIComponent(filename)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('PDF not found');
                    }
                    return response.blob();
                })
                .then(blob => {
                    // Create download link
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    
                    // Cleanup
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    // Re-enable download button
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Registration PDF';
                })
                .catch(error => {
                    console.error("Download error:", error);
                    alert("Error downloading PDF. Please check your email for the registration document.");
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Registration PDF';
                });
        } else {
            alert("PDF not available. Please check your email for the registration document.");
        }
    } catch (error) {
        console.error("Download error:", error);
        alert("Error downloading PDF. Please try again later.");
    }
}

function goToHome() {
    try {
        // Clear all enrollment-related localStorage data
        localStorage.removeItem("formData");
        localStorage.removeItem("hasFiles");
        localStorage.removeItem("photoFile");
        localStorage.removeItem("passportPhotoFile");
        localStorage.removeItem("signatureFile");
        localStorage.removeItem("registrationNumber");
        localStorage.removeItem("pdfUrl");
        localStorage.removeItem("studentName");
        localStorage.removeItem("studentEmail");
        localStorage.removeItem("registrationStatus");
        
        window.location.href = "../index.html";
    } catch (error) {
        console.error("Navigation error:", error);
    }
}

/* ============================================================
   CONFETTI ANIMATION
============================================================ */

const confetti = {
    particles: [],
    colors: ["#F5A623", "#1B2A6B", "#E05A0C", "#10B981", "#3B82F6"],
    
    createParticle() {
        return {
            x: Math.random() * confettiCanvas.width,
            y: -10,
            size: Math.random() * 10 + 5,
            color: this.colors[Math.floor(Math.random() * this.colors.length)],
            speedY: Math.random() * 3 + 2,
            speedX: Math.random() * 4 - 2,
            rotation: Math.random() * 360,
            rotationSpeed: Math.random() * 10 - 5
        };
    },
    
    init() {
        confettiCanvas.width = window.innerWidth;
        confettiCanvas.height = window.innerHeight;
        this.particles = [];
        
        for (let i = 0; i < 150; i++) {
            this.particles.push(this.createParticle());
        }
    },
    
    update() {
        this.particles.forEach((particle, index) => {
            particle.y += particle.speedY;
            particle.x += particle.speedX;
            particle.rotation += particle.rotationSpeed;
            
            if (particle.y > confettiCanvas.height) {
                this.particles[index] = this.createParticle();
            }
        });
    },
    
    draw() {
        const ctx = confettiCanvas.getContext("2d");
        ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
        
        this.particles.forEach(particle => {
            ctx.save();
            ctx.translate(particle.x, particle.y);
            ctx.rotate((particle.rotation * Math.PI) / 180);
            ctx.fillStyle = particle.color;
            ctx.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size);
            ctx.restore();
        });
    },
    
    animate() {
        this.update();
        this.draw();
        confettiAnimationId = requestAnimationFrame(() => this.animate());
    },
    
    start() {
        this.init();
        this.animate();
        
        confettiTimer = setTimeout(() => {
            this.stop();
        }, CONFIG.confettiDuration);
    },
    
    stop() {
        if (confettiAnimationId) {
            cancelAnimationFrame(confettiAnimationId);
            confettiAnimationId = null;
        }
        
        const ctx = confettiCanvas.getContext("2d");
        ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
    }
};

function startConfetti() {
    try {
        confetti.start();
    } catch (error) {
        console.error("Confetti error:", error);
    }
}

/* ============================================================
   EVENT LISTENERS
============================================================ */

function setupEventListeners() {
    downloadBtn.addEventListener("click", downloadPDF);
    homeBtn.addEventListener("click", goToHome);
    
    window.addEventListener("resize", () => {
        if (confettiCanvas) {
            confettiCanvas.width = window.innerWidth;
            confettiCanvas.height = window.innerHeight;
        }
    });
}

/* ============================================================
   INITIALIZATION
============================================================ */

function init() {
    try {
        setupEventListeners();
        
        const registrationStatus = localStorage.getItem("registrationStatus");
        const registrationNumberValue = localStorage.getItem("registrationNumber");
        
        if (registrationStatus === "success" && registrationNumberValue) {
            updateRegistrationNumber();
            setDownloadReady();
            transitionToSuccess();
            return;
        }

        if (registrationNumberValue) {
            updateRegistrationNumber();
            setProcessingState("Your registration is being processed. Your PDF and confirmation email will be ready shortly.");
            transitionToSuccess();
            pollEnrollmentStatus();
            return;
        }

        startProgress();
        startMessageAnimation();
        pollEnrollmentStatus();
    } catch (error) {
        console.error("Initialization error:", error);
    }
}

/* ============================================================
   CLEANUP ON PAGE UNLOAD
============================================================ */

window.addEventListener("beforeunload", () => {
    clearAllTimers();
});

/* ============================================================
   START
============================================================ */

document.addEventListener("DOMContentLoaded", init);