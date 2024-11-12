document.addEventListener('DOMContentLoaded', function () {
    const data=window.userdata
    const profilePicture=document.getElementById("profilePicture")
    const branch=document.getElementById("branch")
    const bio=document.getElementById("bio")
    const username= document.getElementById("username")
    const projects=window.userdata.projects
    
    
    profilePicture.src=data.profilePicture
    branch.textContent=data.branch
    bio.textContent=data.bio
    username.textContent+=data.username
    document.getElementById("viewCount").innerHTML+=`Bugün ${data.viewCount} kişi tarafından görüntülendi.`


    window.openModal = function openModal(index) {
        const nesne=window.userdata.projects[index];
        console.log(nesne)
        const title=nesne.title;
        const description=nesne.description;
        const mediaPath=nesne.media_path;
        document.getElementById("modalTitle").textContent = title;
        document.getElementById("modalDescription").textContent = description;
        const modalMedia = document.getElementById("modalMedia");
        modalMedia.innerHTML = "";  
        if (mediaPath.endsWith('.mp4') || mediaPath.endsWith('.mov')) {
            const video = document.createElement("video");
            video.controls = true;
            video.className = "w-full rounded-lg";
            const source = document.createElement("source");
            source.src = mediaPath;
            source.type = "video/mp4";
            video.appendChild(source);
            modalMedia.appendChild(video);
        } else {
            const img = document.createElement("img");
            img.src = mediaPath;
            img.alt = title;
            img.className = "w-full rounded-lg";
            modalMedia.appendChild(img);
        }

        document.getElementById("projectModal").classList.remove("hidden");
    }

window.closeModal=    function closeModal() {
        document.getElementById("projectModal").classList.add("hidden");
    }

});