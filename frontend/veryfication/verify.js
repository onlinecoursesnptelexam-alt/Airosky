const form=document.getElementById("verifyForm");

const loading=document.getElementById("loading");

const result=document.getElementById("result");

const invalid=document.getElementById("invalid");

const API_BASE_URL = "https://aerosky-institute-vvot.onrender.com";

const certificateIdFromUrl = new URLSearchParams(window.location.search).get("certificateId");

if (certificateIdFromUrl) {

    document.getElementById("certificateId").value = certificateIdFromUrl;

}

form.addEventListener("submit",async function(e){

    e.preventDefault();

    loading.style.display="block";

    result.style.display="none";

    invalid.style.display="none";

    const certificateId=document
    .getElementById("certificateId")
    .value
    .trim();

    try{

        const response = await fetch(
             `${API_BASE_URL}/api/verify/${certificateId}`
        );

        loading.style.display="none";

        if(!response.ok){

            invalid.style.display="block";

            return;

        }

        const data=await response.json();

        document.getElementById("r-id").textContent=
        data.certificate_id;

        document.getElementById("r-name").textContent=
        data.student_name;

        document.getElementById("r-course").textContent=
        data.course;

        document.getElementById("r-date").textContent=
        data.issue_date;

        document.getElementById("r-status").textContent=
        data.status;

        // View PDF

        document.querySelector(".view-btn")
        .href=data.certificate_url;

        document.querySelector(".view-btn")
        .target="_blank";

        // Download PDF

        document.querySelector(".download-btn")
        .href=data.certificate_url;

        document.querySelector(".download-btn")
        .setAttribute("download","");

        result.style.display="block";

    }

    catch(err){

        loading.style.display="none";

        invalid.style.display="block";

        console.log(err);

    }

});