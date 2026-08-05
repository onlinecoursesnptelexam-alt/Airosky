// app.js

console.log("app.js loaded successfully.");

// Use the production backend
const API_BASE_URL = "https://aerosky-institute-vvot.onrender.com";

const form = document.getElementById("studentForm");
const message = document.getElementById("message");

if (!form) {
    console.log("Student form not found on this page.");
} else {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        console.log("Submit button clicked.");

        if (message) {
            message.innerHTML = "";
            message.style.color = "black";
        }

        const photoFile = document.getElementById("photo")?.files[0] || null;
        const passportPhotoFile = document.getElementById("passport_photo")?.files[0] || null;
        const signatureFile = document.getElementById("signature")?.files[0] || null;

        const data = {
            student_name: document.getElementById("student_name")?.value.trim() || "",
            date_of_birth: document.getElementById("date_of_birth")?.value.trim() || "",
            gender: document.getElementById("gender")?.value.trim() || "",
            nationality: document.getElementById("nationality")?.value.trim() || "",
            father_name: document.getElementById("father_name")?.value.trim() || "",
            mother_name: document.getElementById("mother_name")?.value.trim() || "",
            parent_mobile: document.getElementById("parent_mobile")?.value.trim() || "",
            email: document.getElementById("email")?.value.trim() || "",
            age: parseInt(document.getElementById("age")?.value || "0", 10),
            village: document.getElementById("village")?.value.trim() || "",
            post_office: document.getElementById("post_office")?.value.trim() || "",
            district: document.getElementById("district")?.value.trim() || "",
            state: document.getElementById("state")?.value.trim() || "",
            pincode: document.getElementById("pincode")?.value.trim() || "",
            mobile: document.getElementById("mobile")?.value.trim() || "",
            contact_email: document.getElementById("contact_email")?.value.trim() || "",
            emergency_name: document.getElementById("emergency_name")?.value.trim() || "",
            emergency_mobile: document.getElementById("emergency_mobile")?.value.trim() || "",
            emergency_relation: document.getElementById("emergency_relation")?.value.trim() || "",
            qualification: document.getElementById("qualification")?.value.trim() || "",
            board_college: document.getElementById("board_college")?.value.trim() || "",
            passing_year: document.getElementById("passing_year")?.value.trim() || ""
        };

        console.log("Sending Data:", data);

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
            !data.passing_year
        ) {
            if (message) {
                message.style.color = "red";
                message.innerHTML = "Please fill all required fields including photo.";
            }
            return;
        }

        const formData = new FormData();
        formData.append("student_name", data.student_name);
        formData.append("date_of_birth", data.date_of_birth);
        formData.append("gender", data.gender);
        formData.append("nationality", data.nationality);
        formData.append("father_name", data.father_name);
        formData.append("mother_name", data.mother_name);
        formData.append("parent_mobile", data.parent_mobile);
        formData.append("email", data.email);
        formData.append("age", String(data.age));
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

        try {
            if (message) {
                message.innerHTML = "Processing your enrollment...";
                message.style.color = "#F97316";
            }

            const response = await fetch(`${API_BASE_URL}/submit`, {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            console.log("Server Response:", result);

            if (!response.ok || !result.registration_number) {
                throw new Error(result.message || "Enrollment failed");
            }

            localStorage.setItem("registrationNumber", result.registration_number || "AIR-000000-00000");
            localStorage.setItem("studentName", data.student_name);
            localStorage.setItem("studentEmail", data.email);
            localStorage.setItem("registrationStatus", "processing");
            localStorage.removeItem("formData");
            localStorage.removeItem("hasFiles");
            localStorage.removeItem("photoFile");
            localStorage.removeItem("passportPhotoFile");
            localStorage.removeItem("signatureFile");

            window.location.replace("success.html");
        } catch (error) {
            console.error("Enrollment submission error:", error);
            if (message) {
                message.style.color = "red";
                message.innerHTML = error.message || "Error processing files. Please try again.";
            }
        }
    });
}