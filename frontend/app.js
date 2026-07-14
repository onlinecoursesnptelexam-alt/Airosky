// app.js

console.log("app.js loaded successfully.");

// Update this URL for production deployment
const API_BASE_URL = "https://aerosky-institute-vvot.onrender.com";

const form = document.getElementById("studentForm");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    console.log("Submit button clicked.");

    // Clear previous message
    message.innerHTML = "";
    message.style.color = "black";

    // Read form values
    const photoFile = document.getElementById("photo").files[0];
    const passportPhotoFile = document.getElementById("passport_photo") ? document.getElementById("passport_photo").files[0] : null;
    const signatureFile = document.getElementById("signature") ? document.getElementById("signature").files[0] : null;
    const data = {
        student_name: document.getElementById("student_name").value.trim(),
        date_of_birth: document.getElementById("date_of_birth").value.trim(),
        gender: document.getElementById("gender").value.trim(),
        nationality: document.getElementById("nationality").value.trim(),
        father_name: document.getElementById("father_name").value.trim(),
        mother_name: document.getElementById("mother_name").value.trim(),
        parent_mobile: document.getElementById("parent_mobile").value.trim(),
        email: document.getElementById("email").value.trim(),
        age: parseInt(document.getElementById("age").value),
        village: document.getElementById("village").value.trim(),
        post_office: document.getElementById("post_office").value.trim(),
        district: document.getElementById("district").value.trim(),
        state: document.getElementById("state").value.trim(),
        pincode: document.getElementById("pincode").value.trim(),
        mobile: document.getElementById("mobile").value.trim(),
        contact_email: document.getElementById("contact_email").value.trim(),
        emergency_name: document.getElementById("emergency_name").value.trim(),
        emergency_mobile: document.getElementById("emergency_mobile").value.trim(),
        emergency_relation: document.getElementById("emergency_relation").value.trim(),
        qualification: document.getElementById("qualification").value.trim(),
        board_college: document.getElementById("board_college").value.trim(),
        passing_year: document.getElementById("passing_year").value.trim()
    };

    console.log("Sending Data:", data);

    // Basic validation
    if (
        !data.student_name ||
        !data.date_of_birth ||
        !data.gender ||
        !data.nationality ||
        !data.father_name ||
        !data.mother_name ||
        !data.parent_mobile ||
        !data.email ||
        !data.age ||
        !photoFile ||
        !data.village ||
        !data.post_office ||
        !data.district ||
        !data.state ||
        !data.pincode ||
        !data.mobile ||
        !data.contact_email ||
        !data.emergency_name ||
        !data.emergency_mobile ||
        !data.emergency_relation ||
        !data.qualification ||
        !data.board_college ||
        !data.passing_year ||
        !signatureFile
    ) {
        message.style.color = "red";
        message.innerHTML = "Please fill all fields including photo and signature.";
        return;
    }

    // Save form data to localStorage for success page to process
    localStorage.setItem("formData", JSON.stringify(data));
    localStorage.setItem("hasFiles", "true");

    // Convert files to base64 and save
    const fileToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    };

    try {
        const photoBase64 = await fileToBase64(photoFile);
        localStorage.setItem("photoFile", photoBase64);

        if (passportPhotoFile) {
            const passportBase64 = await fileToBase64(passportPhotoFile);
            localStorage.setItem("passportPhotoFile", passportBase64);
        }

        if (signatureFile) {
            const signatureBase64 = await fileToBase64(signatureFile);
            localStorage.setItem("signatureFile", signatureBase64);
        }

        // Redirect immediately to success page
        window.location.href = "success.html";

    } catch (error) {
        console.error("File conversion error:", error);
        message.style.color = "red";
        message.innerHTML = "Error processing files. Please try again.";
    }

});