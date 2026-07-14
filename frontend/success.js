/* ============================================================
   AIROSKY SUCCESS PAGE
   success.js
   Complete Production-Ready Implementation

============================================================ */

/* ============================================================
   CONFIGURATION
============================================================ */

// Update this URL for production deployment
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
        status: localStorage.getItem("registrationStatus") || "success"
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

/* ============================================================
   BACKGROUND FORM SUBMISSION
============================================================ */

async function submitFormInBackground() {
    try {
        const formDataStr = localStorage.getItem("formData");
        const hasFiles = localStorage.getItem("hasFiles");

        if (!formDataStr || hasFiles !== "true") {
            console.log("No form data to submit");
            return;
        }

        const data = JSON.parse(formDataStr);
        const photoBase64 = localStorage.getItem("photoFile");
        const passportPhotoBase64 = localStorage.getItem("passportPhotoFile");
        const signatureBase64 = localStorage.getItem("signatureFile");

        // Convert base64 to File objects
        const base64ToFile = (base64, filename) => {
            const arr = base64.split(',');
            const mime = arr[0].match(/:(.*?);/)[1];
            const bstr = atob(arr[1]);
            let n = bstr.length;
            const u8arr = new Uint8Array(n);
            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new File([u8arr], filename, { type: mime });
        };

        const photoFile = base64ToFile(photoBase64, `${data.student_name.replace(' ', '_')}_photo.jpg`);
        let passportPhotoFile = null;
        let signatureFile = null;

        if (passportPhotoBase64) {
            passportPhotoFile = base64ToFile(passportPhotoBase64, `${data.student_name.replace(' ', '_')}_passport.jpg`);
        }

        if (signatureBase64) {
            signatureFile = base64ToFile(signatureBase64, `${data.student_name.replace(' ', '_')}_signature.jpg`);
        }

        // Create FormData
        const formData = new FormData();
        formData.append("student_name", data.student_name);
        formData.append("date_of_birth", data.date_of_birth);
        formData.append("gender", data.gender);
        formData.append("nationality", data.nationality);
        formData.append("father_name", data.father_name);
        formData.append("mother_name", data.mother_name);
        formData.append("parent_mobile", data.parent_mobile);
        formData.append("email", data.email);
        formData.append("age", data.age);
        formData.append("photo", photoFile);
        formData.append("village", data.village);
        formData.append("post_office", data.post_office);
        formData.append("district", data.district);
        formData.append("state", data.state);
        formData.append("pincode", data.pincode);
        if (passportPhotoFile) {
            formData.append("passport_photo", passportPhotoFile);
        }
        formData.append("mobile", data.mobile);
        formData.append("contact_email", data.contact_email);
        formData.append("emergency_name", data.emergency_name);
        formData.append("emergency_mobile", data.emergency_mobile);
        formData.append("emergency_relation", data.emergency_relation);
        formData.append("qualification", data.qualification);
        formData.append("board_college", data.board_college);
        formData.append("passing_year", data.passing_year);
        if (signatureFile) {
            formData.append("signature", signatureFile);
        }

        const response = await fetch(`${API_BASE_URL}/submit`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        console.log("Server Response:", result);

        if (response.ok && result.status === "success") {
            // Save result to localStorage
            localStorage.setItem("registrationNumber", result.registration_number || "AIR-000000-00000");
            localStorage.setItem("pdfUrl", result.pdf || "");
            localStorage.setItem("studentName", data.student_name);
            localStorage.setItem("studentEmail", data.email);
            localStorage.setItem("registrationStatus", "success");

            // Clear form data from localStorage
            localStorage.removeItem("formData");
            localStorage.removeItem("hasFiles");
            localStorage.removeItem("photoFile");
            localStorage.removeItem("passportPhotoFile");
            localStorage.removeItem("signatureFile");

            // Update registration number on success page immediately with the correct ID from backend
            if (result.registration_number && registrationNumber) {
                registrationNumber.textContent = result.registration_number;
            }

            // Now transition to success screen with correct registration number
            transitionToSuccess();

        } else {
            console.error("Server error:", result.message);
            localStorage.setItem("registrationStatus", "error");
            alert("Error: " + (result.message || "Failed to process enrollment"));
            // Still transition to show error
            transitionToSuccess();
        }

    } catch (error) {
        console.error("Background submission error:", error);
        localStorage.setItem("registrationStatus", "error");
        // Still transition to show error state
        transitionToSuccess();
    }
}

/* ============================================================
   BUTTON FUNCTIONS
============================================================ */

function downloadPDF() {
    try {
        const data = getStudentData();
        
        if (data.pdf) {
            // Extract filename from pdf path
            const filename = data.pdf.split('/').pop();
            
            // Fetch PDF from backend
            fetch(`${API_BASE_URL}/download-pdf/${filename}`)
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
                })
                .catch(error => {
                    console.error("Download error:", error);
                    alert("Error downloading PDF. Please check your email for the registration document.");
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
        startProgress();
        startMessageAnimation();
        
        // Submit form in background
        submitFormInBackground();
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