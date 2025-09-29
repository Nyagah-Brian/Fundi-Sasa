document.addEventListener("DOMContentLoaded", () => {
    const services = ["Plumbing","Painting","Electrical","Carpentry","Cleaning","AC Repair","Roofing","Gardening"];
    const servicesList = document.getElementById('services');
    const locationModal = document.getElementById('location-modal');
    const modalLocationInput = document.getElementById('modal-location');
    let selectedSkill = '';

    // Populate service cards
    services.forEach(skill => {
        const li = document.createElement('li');
        li.className = 'service-card';
        li.textContent = skill;
        li.onclick = () => openLocationModal(skill);
        servicesList.appendChild(li);
    });

    // Open modal
    function openLocationModal(skill) {
        selectedSkill = skill;
        modalLocationInput.value = '';
        locationModal.style.display = 'flex';
    }

    // Confirm modal
    document.getElementById('confirm-location').onclick = () => {
        const location = modalLocationInput.value.trim();
        if (!location) return alert("Location required");
        sessionStorage.setItem("selectedSkill", selectedSkill);
        sessionStorage.setItem("selectedLocation", location);
        window.location.href = "technicians.html";
    }

    // Cancel modal
    document.getElementById('cancel-location').onclick = () => {
        locationModal.style.display = 'none';
    }

    // Search button (manual skill input)
    document.getElementById('search-btn').onclick = () => {
        const skillInput = document.getElementById('skill-input').value.trim();
        if (!skillInput) return alert("Please enter a skill");
        selectedSkill = skillInput;
        modalLocationInput.value = '';
        locationModal.style.display = 'flex';
    }

    // Use My Location button
    document.getElementById('my-location-btn').onclick = () => {
        if (!navigator.geolocation) return alert("Geolocation not supported by your browser");
        navigator.geolocation.getCurrentPosition(async (pos) => {
            const { latitude, longitude } = pos.coords;

            // Convert to readable location using OpenStreetMap Nominatim API
            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
                const data = await response.json();
                modalLocationInput.value = data.address.city || data.address.town || data.address.village || `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
            } catch (err) {
                console.error(err);
                modalLocationInput.value = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
            }
        }, (err) => {
            alert("Unable to retrieve location");
        });
    }
});
