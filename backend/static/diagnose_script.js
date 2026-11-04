document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("diagnoseForm");
  const input = document.getElementById("plantInput");
  const previewSection = document.getElementById("previewSection");
  const previewImage = document.getElementById("previewImage");
  const resultSection = document.getElementById("resultSection");
  const resultText = document.getElementById("resultText");

  // Show preview when file selected
  input.addEventListener("change", () => {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        previewImage.src = e.target.result;
        previewSection.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    }
  });


   form.addEventListener("submit", async (e) => {
    e.preventDefault(); // prevent default page reload

    const file = input.files[0];
    if(!file){
        alert("Please upload an image first!");
        return;
    }

    resultSection.classList.remove("hidden");
    resultText.textContent = "Processing your plant image...";

    const formData = new FormData();
    formData.append('image', file);
    formData.append('model','best'); // optional

    try {
        const response = await fetch('/diagnosis/api/detect/', { method: 'POST', body: formData });
        const data = await response.json();

        if(data.error){
            resultText.innerHTML = `<span style="color:red">${data.error}</span>`;
        } else {
            resultText.innerHTML = `
                <strong>Disease:</strong> ${data.disease}<br>
                <strong>Confidence:</strong> ${data.confidence}<br>
                <strong>Recommended Fertilizers:</strong>
                <ul>${data.fertilizers.map(f => `<li>🌱 ${f}</li>`).join('')}</ul>
                <br>
                <strong>Remedies:</strong>
                <ul>${data.remedies.map(r => `<li>💊 ${r}</li>`).join('')}</ul>
            `;
        }
    } catch(err){
        resultText.innerHTML = `<span style="color:red">Error: ${err}</span>`;
    }
});

  });
