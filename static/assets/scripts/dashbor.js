window.onload = function() {
    const username = window.userData.username;
    const profilePictureUrl = window.userData.profilePicture; 
    const branch=window.userData.branch
    const bio=window.userData.bio
    const professionSelect=document.getElementById("professionSelect")
    const youtubeInput = document.getElementById("youtubeInput");
    const linkedinInput = document.getElementById("linkedinInput");
    const instagramInput = document.getElementById("instagramInput");
    const twitterInput = document.getElementById("twitterInput");
    const githubInput = document.getElementById("githubInput");
    const bioInput=document.getElementById("bioInput")
    const viewMyBioButton=document.getElementById("viewMyBioButton")
    const usernameLabel=document.getElementById("usernameLabel")
    viewMyBioButton.addEventListener("click", function() {
        window.location.href = "/@" + username;
    });
    console.log(window.userData);
    usernameLabel.textContent=`Hoşgeldin,${username}!`
    bioInput.value=bio || ''
    professionSelect.value=branch|| '';
    youtubeInput.value = window.userData.social_media.youtube || ''; 
    linkedinInput.value = window.userData.social_media.linkedin || '';
    instagramInput.value = window.userData.social_media.instagram || '';
    twitterInput.value = window.userData.social_media.twitter || '';
    githubInput.value = window.userData.social_media.github || '';
    if (profilePictureUrl) {
        document.getElementById('profilePicture').src = profilePictureUrl;
    } else {
        console.log("Profile picture not available.");
        document.getElementById('profilePicture').src = 'path/to/default/profile/picture.png'; 
    }
};




fetch(`/get-visit-data?username=${window.userData.username}`)  // Replace with dynamic username if needed
.then(response => response.json())
.then(data => {
    // Handle Hourly Visits Data
    const hourlyVisitsData = data.hourlyVisits.data;
    const hourlyLabels = data.hourlyVisits.labels;

    if (hourlyVisitsData.length === 0 || hourlyVisitsData.every(val => val === 0)) {
        document.getElementById('hourlyVisitsSection').innerHTML = `<p>No visit data available for today.</p>`;
    } else {
        const ctxHourly = document.getElementById('hourlyVisitsChart').getContext('2d');
        new Chart(ctxHourly, {
            type: 'line',
            data: {
                labels: hourlyLabels,  // ['00', '01', ..., '23']
                datasets: [{
                    label: 'Hourly Visits',
                    data: hourlyVisitsData,  // [0, 1, 0, 3, ...]
                    fill: false,
                    borderColor: '#4CAF50',  // Green color for the line
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Hour of the Day'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Visit Count'
                        }
                    }
                }
            }
        });
    }

  

    // Display other stats like visit count and most visited country
    document.getElementById('visitCount').innerText = data.visitCount;

})
.catch(error => {
    console.error('Error fetching visit data:', error);
});


    function showSection(section) {
        const sections = ['dashboardSection', 'projectUploadSection', 'bioUpdateSection', 'socialMediaSection',"themeSelectionSection","accountSettingsSection"];

        sections.forEach((sec) => {
            const secElement = document.getElementById(sec);
            console.log(sec, secElement);
            if (secElement) {
                secElement.classList.add('hidden');
            }
        });
    
        const selectedSection = document.getElementById(`${section}Section`);
        if (selectedSection) {
            selectedSection.classList.remove('hidden');
        } else {
            console.error(`Section with ID ${section}Section not found!`);
        }
    }
    


        
    document.addEventListener('DOMContentLoaded', function () {
        // Navbar linkleri
        const logoutLink = document.getElementById('logoutLink');
        const professionError = document.getElementById('professionError');
        const branch_list = document.getElementById("professionSelect");
    
        // Event listener eklemek
       
        if (logoutLink) {
            logoutLink.addEventListener('click', function () {
                logout();
            });
        }
        function openSectionByHash() {
            const hash = window.location.hash.substring(1); // Remove '#' from the hash
        
            switch (hash) {
                case 'dashboard':
                    showSection('dashboard');
                    break;
                case 'projectUpload':
                    showSection('projectUpload');
                    break;
                case 'bioUpdate':
                    showSection('bioUpdate');
                    break;
                case 'themeSelection':
                    showSection('themeSelection');
                    break;
                case 'socialMedia':
                    showSection('socialMedia');
                    break;
                case 'accountSettings':
                    showSection('accountSettings');
                    break
                default:
                    showSection('dashboard'); // Default section
            }
        }
        
        // Run on page load
        window.addEventListener('load', openSectionByHash);
        
        // Run when the hash changes (for example, if the user manually changes the hash)
        window.addEventListener('hashchange', openSectionByHash);
        // Meslek değişimi
        if (branch_list) {
            branch_list.addEventListener('change', async function () {
                const branch = branch_list.value;
                console.log("Seçilen meslek:", branch);
    
                try {
                    const response = await fetch("/update_branch", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ branch: branch })
                    });
    
                    const result = await response.json();
                    if (professionError) {
                        professionError.classList.remove("hidden");
                        professionError.textContent = result.message;  // Mesajı göster
                    }
    
                } catch (error) {
                    console.error('Meslek güncellenirken hata oluştu:', error);
                    alert('Meslek güncellenirken bir hata oluştu.');
                }
            });
        }
    
        const pictureInput = document.getElementById("profilePictureInput");
        if (pictureInput) {
            document.getElementById("profilePicture").addEventListener("click", function () {
                pictureInput.click(); 
            });
    
            pictureInput.addEventListener("change", function (event) {
                const input = event.target;
                if (input.files.length === 0) return;
    
                const file = input.files[0];
                const profilePicture = document.getElementById("profilePicture");
                profilePicture.src = URL.createObjectURL(file);
    
                const formData = new FormData();
                formData.append('file', file);
    
                fetch('/upload_profile_picture', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(result => {
                    const uploadMessage = document.getElementById('uploadProfilePictureMessage');
                    if (uploadMessage) {
                        uploadMessage.textContent = result.message;
                    }
                })
                .catch(error => {
                    console.error('Error uploading profile picture:', error);
                    alert('Resim yüklenirken bir hata oluştu.');
                });
            });
        }
        const checkbox = document.getElementById('toggleCheckbox');
        const toggleCircle = document.getElementById('toggleCircle');
        const accountSettingsMessage = document.getElementById("accountSettingsMessage");
        let svalue = 0;
        svalue = window.userData.status_2fa;  // Backend'den gelen değer 0 ya da 1 olabilir
        if (svalue === 1) {
                checkbox.checked = true;  // Checkbox'ı işaretle
                toggleCircle.style.transform = 'translateX(1.25rem)'; // Sağ kaydır
                toggleCircle.style.backgroundColor = '#3B82F6'; // Mavi renk
                toggleCircle.style.borderColor = 'white'; // Beyaz sınır
                } else {
                checkbox.checked = false;  // Checkbox'ı işaretini kaldır
                toggleCircle.style.transform = 'translateX(0)'; // Başlangıçta solda
                toggleCircle.style.backgroundColor = 'white'; // Beyaz renk
                toggleCircle.style.borderColor = '#D1D5DB'; // Gri sınır
                }

        
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                toggleCircle.style.transform = 'translateX(1.25rem)'; // Sağ kaydırma
                toggleCircle.style.backgroundColor = '#3B82F6'; // Mavi renk
                toggleCircle.style.borderColor = 'white'; // Beyaz sınır
                svalue = 1;
            } else {
                toggleCircle.style.transform = 'translateX(0)'; // Başlangıçta solda
                toggleCircle.style.backgroundColor = 'white'; // Beyaz renk
                toggleCircle.style.borderColor = '#D1D5DB'; // Gri sınır
                svalue = 0;
            }
    
            // Yeni durumu backend'e gönder
            fetch(`/switch_2FA?status=${svalue}`, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(result => {
                accountSettingsMessage.textContent = result.message;
            })
            .catch(error => {
                console.error('2FA durumu güncellenirken hata oluştu:', error);
                accountSettingsMessage.textContent = "2FA durumu güncellenirken hata oluştu.";
            });
        });

       
    });
    
    
    
async function logout() {
    try {
        const response = await fetch('/logout', { method: 'POST' });
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('Çıkış yaparken bir hata oluştu.');
        }
    } catch (error) {
        console.error('Logout failed:', error);
        alert('Çıkış yaparken bir hata oluştu.');
    }
}





async function loadExistingProjects() {
    try {
        const response = await fetch('/get_projects');
        const result = await response.json();
        const projectsContainer = document.getElementById('existingProjectsContainer');
        projectsContainer.innerHTML = ''; // Önceki projeleri temizle

        if (result.projects && result.projects.length > 0) {
            result.projects.forEach(project => {
                const projectDiv = document.createElement('div');
                projectDiv.className = "border p-4 rounded-lg shadow";
                projectDiv.innerHTML = `
                    <h3 class="font-bold text-lg">${project.title}</h3>
                    <p class="text-gray-600">${project.description}</p>
                    <a href="${project.media_path}" class="text-blue-600 underline hover:text-blue-800" target="_blank">Videoyu izle</a>
                `;
                projectsContainer.appendChild(projectDiv);
            });
        } else {
            projectsContainer.innerHTML = '<p class="text-gray-500">Hiç proje bulunamadı.</p>';
        }
    } catch (error) {
        console.error('Failed to load projects:', error);
        alert('Projeler yüklenirken bir hata oluştu.');
    }
}

document.getElementById('uploadProjectButton').addEventListener('click', async () => {
    const title = document.getElementById('projectTitle').value;
    const description = document.getElementById('projectDescription').value;
    const mediaFile = document.getElementById('projectMedia').files[0];

    if (mediaFile && mediaFile.size > 30 * 1024 * 1024) {
        alert('Dosya boyutu 30MB\'ı geçemez.');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    if (mediaFile) {
        formData.append('media', mediaFile);
    }

    try {
        const response = await fetch('/upload_project', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('uploadProjectMessage').textContent = result.message;

        document.getElementById('projectTitle').value = '';
        document.getElementById('projectDescription').value = '';
        document.getElementById('projectMedia').value = '';
        document.getElementById('previewContainer').innerHTML = '';

        await loadExistingProjects();
    } catch (error) {
        console.error('Failed to upload project:', error);
        alert('Proje yüklenirken bir hata oluştu.');
    }
});


document.getElementById("updateSocialMediaButton").addEventListener("click",async()=>{
    const youtubeInput=document.getElementById("youtubeInput")
    const linkedinInput=document.getElementById("linkedinInput")
    const instagramInput=document.getElementById("instagramInput")
    const twitterInput=document.getElementById("twitterInput")

    try{

        const response=await fetch("/update_social_media",{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                youtube:youtubeInput.value,
                instagram:instagramInput.value,
                twitter:twitterInput.value,
                linkedin:linkedinInput.value,
                github:githubInput.value


            })
        })
        const result=await response.json();
        document.getElementById("updateSocialMediaMessage").textContent=result.message;
    } catch (error) {
        console.error('Failed to update bio:', error);
        alert('Bio güncellenirken bir hata oluştu.');
    }
});






document.getElementById('updateBioButton').addEventListener('click', async () => {
    const bio = document.getElementById('bioInput').value;

    try {
        const response = await fetch('/update_bio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ bio: bio })
        });

        const result = await response.json();
        document.getElementById('updateBioMessage').textContent = result.message;


    } catch (error) {
        console.error('Failed to update bio:', error);
        alert('Bio güncellenirken bir hata oluştu.');
    }
});
loadExistingProjects();