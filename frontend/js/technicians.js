document.addEventListener("DOMContentLoaded", () => {
    const skill = sessionStorage.getItem("selectedSkill");
    const location = sessionStorage.getItem("selectedLocation");

    const subtitle = document.getElementById("subtitle");
    const loader = document.getElementById("loader");
    const techList = document.getElementById("technician-list");
    const noResults = document.getElementById("no-results");

    subtitle.textContent = `Skill: ${skill} | Location: ${location}`;
    loader.style.display = 'block';

    fetch(`http://127.0.0.1:5000/technicians/recommend?skill=${encodeURIComponent(skill)}&location=${encodeURIComponent(location)}`)
        .then(res => res.json())
        .then(data => {
            const technicians = data.recommendations || [];
            loader.style.display = 'none';

            if (technicians.length === 0) {
                noResults.style.display = 'block';
                return;
            }

            technicians.forEach(tech => {
                const li = document.createElement('li');
                li.className = 'tech-card';

                const skillBadges = tech.skills.split(',').map(s => `<span class="skill-badge">${s.trim()}</span>`).join(' ');

                li.innerHTML = `
                    <img src="images/placeholder.jpg" alt="Tech Photo">
                    <h3>${tech.name}</h3>
                    <p>Location: ${tech.location}</p>
                    <p>Price: $${tech.price_rate}/hr</p>
                    <p>Rating: ${tech.avg_rating} ⭐</p>
                    <p>Skills: ${skillBadges}</p>
                `;

                techList.appendChild(li);
            });
        })
        .catch(err => {
            console.error(err);
            loader.style.display = 'none';
            noResults.style.display = 'block';
            noResults.textContent = 'Error fetching technicians.';
        });
});
