window.onload = function() {
    const userCountElement = document.getElementById("userCount");
    const pageData=window.data.pageData
    const button1=document.getElementById("button1")
    const button2=document.getElementById("button2")
    console.log
    button1.href=pageData[1]
    button2.href=pageData[1]
    button1.textContent=pageData[0]
    button2.textContent=pageData[0]



    if (userCountElement) {
        userCountElement.textContent = window.data.userCount;
    } else {
        console.log("userCount öğesi bulunamadı!");
    }
    document.getElementById("generateLink").addEventListener("click", function() {
        const url = `/auth`;
        window.location.href = url;
    });
};